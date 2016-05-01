#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from functools import partial
from hashlib import md5
from itertools import groupby
from os import walk
from os.path import exists, getmtime, join
import re

try:
    import Image
except ImportError:
    from PIL import Image

from bs4 import BeautifulSoup
from flask import (Flask, Markup, make_response, redirect, render_template,
    request)
from markdown import markdown as render_markdown
import typogrify.filters
import yaml

from memoize import MetaMemoize
from post_collection import PostCollectionRecipe
import settings


HTTP_404 = '404', 404
app = Flask(__name__)


class memoized(object):
    __metaclass__ = MetaMemoize

    def asset_relative_paths():
        """
        Paths relative to ASSETS_DIR.
        """

        paths = []

        for root, dirnames, filenames in walk(settings.ASSETS_DIR):
            dir_ = root[len(settings.ASSETS_DIR):].lstrip('/')
            for filename in filenames:
                if not filename.startswith('.'):
                    paths.append(join(dir_, filename))

        return paths

    def collections():
        recipes = [
            PostCollectionRecipe("Checkers series",
                predicate=lambda post: 'checkers' in post['slug']),

            PostCollectionRecipe("Setup series", slugs=[
                'menu-bar',
                '5k-imac',
                'mac-software',
            ]),

            PostCollectionRecipe("Procedural series", slugs=[
                'shattered-polygons',
                'sketchy-procedures',
                'xero',
                'bytebeat',
            ]),
        ]

        posts = sorted(memoized.public_posts(), key=lambda x: x['date'])
        return [r.collection_with_posts(posts) for r in recipes]

    def draft_filenames():
        return public_filnames_in_directory(settings.DRAFTS_DIR)

    def post_data(filename):
        # is post a draft?
        is_draft = filename in memoized.draft_filenames()
        title_prefix = 'DRAFT: ' if is_draft else ''
        directory = settings.DRAFTS_DIR if is_draft else settings.POSTS_DIR

        # get post split into sections
        separator = '\n\n'
        with open(join(directory, filename)) as f:
            sections = f.read().decode('utf8').split(separator)

        # get data from sections
        slug = filename[:-len('.md')]
        title = title_prefix + sections[1].rstrip('=').rstrip('\n')
        path = '/posts/%s' % slug
        return {
            'is_draft': is_draft,
            'date': sections[0],
            'title': title,
            'stupified_title': stupify(title),
            'remaining_markdown': separator.join(sections[2:]),
            'slug': slug,
            'stupified_slug': stupify(slug),
            'path': path,
            'url': 'http://narf.pl%s' % path,
        }

    def post_filenames():
        return public_filnames_in_directory(settings.POSTS_DIR)

    def public_posts():
        return antimap(memoized.post_filenames(), [
            partial(map, memoized.post_data),
            partial(filter, lambda x: not x['is_draft']),
            partial(sorted, key=lambda x: x['date'], reverse=True),
        ])

    def rendered_feed():
        # get entries from YAML
        path = join(settings.CONTENT_DIR, 'feed.yaml')
        with open(path) as f:
            entries = yaml.load(f)

        # add posts
        for filename in memoized.post_filenames():
            dct = memoized.post_data(filename)

            if dct['is_draft']:
                continue

            entries.append({
                'title': dct['title'],
                'time': '%s 00:00' % dct['date'],
                'link': dct['url'],
            })

        # set "updated" field (ISO 8601) in a retarded manner
        for e in entries:
            e['updated'] = '%s:00+01:00' % e['time'].replace(' ', 'T')

        # sort entries by update time
        entries = sorted(entries, reverse=True, key=lambda e: e['updated'])

        return render_template('feed.xml', entries=entries)

    def rendered_index():
        html = render_template('index.html')

        # dirty hack!
        return resolve_asset_urls('index.md', html)

    def rendered_post(filename):
        # get post data
        ctx = memoized.post_data(filename)

        # render and process markdown
        ctx['content'] = antimap(ctx['remaining_markdown'], [
            render_markdown,
            wrap_images_in_figures_instead_of_paragraphs,
            turn_mp4_images_to_videos,
            partial(resolve_asset_urls, filename),
            center_figure_captions,
            wrap_images_in_links,
            thumbnail_big_images,
            add_max_height_class_to_images,
            add_footnote_links,
        ])

        # add collection info
        for collection in memoized.collections():
            if collection.contains_post(ctx):
                ctx['collection_navigation_item'] = \
                     collection.navigation_item_for_post(ctx)
                break

        # get dedicated social image
        social_image_url = None
        relative_path = '%s/social.jpg' % filename[:-len('.md')]
        if relative_path in memoized.asset_relative_paths():
            social_image_url = '/thumbnails/' + relative_path

        # use first image as social image
        if social_image_url is None:
            soup = BeautifulSoup(ctx['content'])
            for img in soup.find_all('img'):
                social_image_url = img['src']
                break

        # add domain and set social image
        if social_image_url:
            if social_image_url.startswith('/'):
                social_image_url = 'http://narf.pl' + social_image_url

            ctx['social_image_url'] = social_image_url

        # render final html
        html = render_template('post.html', **ctx)
        return add_title_text_to_post_links(html)

    def rendered_posts():
        posts = memoized.public_posts()
        get_year = lambda x: x['date'].split('-')[0]

        return render_template('posts.html',
            selected_posts=memoized.selected_posts(),
            posts_by_year=groupby(posts, get_year))

    def selected_posts():
        selected_slugs = [
            'bytebeat',
            'lenses-in-swift',
            '5k-imac',
            'checkers-explosion-bug',
            'music-streaming',
            'pegasus',
        ]

        predicate = lambda post: post['slug'] in selected_slugs

        return filter(predicate, memoized.public_posts())

    def static_url():
        if app.debug:
            return '/static'
        else:
            return 'http://static.narf.pl/main'

    def static_url_for_asset(path):
        # 'a/b/c' → '/static/assets/a/b/c?sdfsdfsdf'
        mtime = getmtime(join(settings.ASSETS_DIR, path))
        base = memoized.static_url()
        return '%s/assets/%s?%s' % (base, path, get_hash(mtime))

    def static_url_for_thumbnail(path):
        # 'a/b/c.jpg' → '/static/thumbnails/sdfsdfsdf.jpg'

        # get asset data
        asset_path = join(settings.ASSETS_DIR, path)
        mtime = getmtime(asset_path)
        image = Image.open(asset_path)
        width, height = image.size

        # set size limits
        max_width = 1024 * 2
        max_height = 780 * 2

        # ignore max height for selected images
        if '@max-height' in path:
            max_height = height

        # don't scale small images
        if width <= max_width and height <= max_height:
            return memoized.static_url_for_asset(path)

        # create hashed filename
        filename = '%s.jpg' % get_hash('%s:%f:%d:%d' % \
                                       (path, mtime, max_width, max_height))
        thumbnail_path = join(settings.THUMBNAILS_DIR, filename)
        base = memoized.static_url()
        url = '%s/thumbnails/%s' % (base, filename)

        # create thumbnail if it doesn't exist
        if not exists(thumbnail_path):
            image.thumbnail((max_width, max_height), Image.ANTIALIAS)
            image.save(thumbnail_path, "JPEG", quality=95)

        return url


def antimap(x, functions):
    """
    `antimap(x, [f, g])` == `g(f(x))`
    """

    for f in functions:
        x = f(x)

    return x


def add_footnote_links(html):
    # replace all "[numbers]" with "<sup>" links
    pattern = re.compile(r'([^\s])\[(\d+)\]([^\w])')
    def repl(match):
        repl.was_called = True
        return '%s<a href="#footnotes"><sup>%s</sup></a>%s' % match.groups()

    # perform replacement
    html = pattern.sub(repl, html)

    # wrap last <hr> in <a name>
    if getattr(repl, 'was_called', True):
        html = '<a name="footnotes"><hr></a>'.join(html.rsplit('<hr/>', 1))

    return html


def add_max_height_class_to_images(html):
    """
    >>> add_max_height_class_to_images('<img src="foo@max-height.jpg">')
    u'<img src="foo@max-height.jpg" class="max-height">'
    """

    soup = BeautifulSoup(html)

    for img in soup.find_all('img'):
        if '@max-height' in img['src']:
            img['class'] = ' '.join(filter(None, [
                img.get('class'),
                'max-height',
            ]))

    return unicode(soup)


def add_title_text_to_post_links(html):
    prefixes = ['/posts', 'http://narf.pl/posts']
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        url = link.get('href', '')

        if any(url.startswith(x) for x in prefixes):
            slug = url.split('/')[-1]

            for post in memoized.public_posts():
                if post['slug'] == slug:
                    link['title'] = post['title']
                    break

    return unicode(soup)


def center_figure_captions(html):
    soup = BeautifulSoup(html)

    for figure in soup.find_all('figure'):
        # get next paragraph
        p = figure.find_next_sibling('p')
        if p is None:
            continue

        # make sure paragraph is caption
        children = list(p.children)
        if len(children) != 1 or children[0].name != 'em':
            continue

        # center paragraph
        p['class'] = 'narrow centered'

    return unicode(soup)


def get_hash(x):
    return md5(str(x)).hexdigest()


def public_filnames_in_directory(directory):
    for root, dirnames, filenames in walk(directory):
        return [x for x in filenames if not x.startswith('.')]

    return []


def resolve_asset_urls(filename, html):
    """
    >>> resolve_asset_urls('foo.md', '<a href="bar.jpg">baz</a>')
    u'<a href="/assets/foo/bar.jpg">baz</a>'
    """

    slug = filename[:-len('.md')]
    soup = BeautifulSoup(html)

    def change_url(tag, key):
        try:
            url = tag[key]
        except KeyError:
            return

        if not ('//' in url or
                any(url.startswith(x) for x in ['/', '#', 'mailto:'])):
            tag[key] = '/assets/%s/%s' % (slug, url)

    for tag_name, key in [
        ('a', 'href'),
        ('img', 'src'),
        ('script', 'src'),
        ('video', 'src'),
        ('source', 'src'),
    ]:
        for tag in soup.find_all(tag_name):
            change_url(tag, key)

    return unicode(soup)


stupify_regex = re.compile(r'[^a-z0-9]')

def stupify(s):
    """
    Transform string to lowercase and remove non-alphanumeric characters.
    """

    return stupify_regex.sub('', s.lower())


def thumbnail_big_images(html):
    """
    >>> thumbnail_big_images('<img src="/assets/foo.jpg">')
    u'<img src="/thumbnails/foo.jpg">'
    """

    prefix = '/assets/'
    soup = BeautifulSoup(html)

    for img in soup.find_all('img'):
        url = img['src']
        path = url[len(prefix):]

        # check if the image can have a thumbnail
        if url.startswith(prefix) and 'thumbnails' in \
                                      memoized.static_url_for_thumbnail(path):
            # use the thumbnail instead of the original image
            img['src'] = '/thumbnails/%s' % path

    return unicode(soup)


def turn_mp4_images_to_videos(html):
    """
    >>> turn_mp4_images_to_videos('<img src="foo.mp4">')
    u'<video src="foo.mp4" autoplay loop></video>'
    """

    soup = BeautifulSoup(html)

    for img in soup.find_all('img'):
        src = img['src']
        if src.endswith('.mp4'):
            img.replace_with(soup.new_tag('video',
                src=src,
                autoplay='autoplay',
                loop='loop'))

    return unicode(soup)


def wrap_images_in_figures_instead_of_paragraphs(html):
    """
    >>> wrap_images_in_figures_instead_of_paragraphs('<p><img src="/assets/foo.jpg"></p>')
    u'<figure><img src="/assets/foo.jpg"></figure>'
    """

    soup = BeautifulSoup(html)

    for img in soup.find_all('img'):
        # get parent paragraph
        parent = img.parent
        if parent and parent.name == 'a':
            parent = parent.parent

        # change <p> into <figure>
        if parent and parent.name == 'p':
            parent.name = 'figure'

    return unicode(soup)


def wrap_images_in_links(html):
    """
    >>> wrap_images_in_links('<img src="/assets/foo.jpg">')
    u'<a href="/assets/foo.jpg"><img src="/assets/foo.jpg"></a>'
    """

    soup = BeautifulSoup(html)

    for img in soup.find_all('img'):
        if not (img.parent and img.parent.name == 'a'):
            a = soup.new_tag('a')
            a['href'] = img['src']
            a.append(img.replace_with(a))

    return unicode(soup)


@app.template_filter('typo')
def typo_filter(text):
    text = typogrify.filters.widont(text)
    text = typogrify.filters.smartypants(text)
    text = text.replace('OS X', 'OS&nbsp;X')

    return Markup(text)


@app.before_request
def strip_trailing_slash():
    path = request.path
    if path != '/' and path.endswith('/'):
        return redirect(path.rstrip('/'), 301)


@app.route('/')
def index():
    return memoized.rendered_index()


@app.route('/posts')
def posts():
    return memoized.rendered_posts()


@app.route('/posts/<path:slug>')
def post(slug):
    filename = slug + '.md'
    if filename in memoized.post_filenames():
        return memoized.rendered_post(filename)
    else:
        return HTTP_404


@app.route('/drafts/<path:slug>')
def draft(slug):
    filename = slug + '.md'
    if filename in memoized.post_filenames():
        return redirect(memoized.post_data(filename)['path'])
    elif filename in memoized.draft_filenames():
        return memoized.rendered_post(filename)
    else:
        return HTTP_404


@app.route('/feed')
def feed():
    response = make_response(memoized.rendered_feed())
    response.mimetype = 'application/atom+xml'
    return response


@app.route('/assets/<path:path>')
def asset(path):
    if path in memoized.asset_relative_paths():
        return redirect(memoized.static_url_for_asset(path))
    else:
        return HTTP_404


@app.route('/thumbnails/<path:path>')
def thumbnail(path):
    # fail fast
    if path not in memoized.asset_relative_paths():
        return

    # allow only thumbnails of jpgs and pngs
    if not any(path.endswith(x) for x in ['.jpg', '.png']):
        return '418', 418

    # redirect to thumbnail
    return redirect(memoized.static_url_for_thumbnail(path))


@app.route('/cv')
def cv():
    return redirect('https://www.linkedin.com/in/narfdotpl', 302)


@app.route('/checkers')
def checkers():
    return redirect('/posts/glitchy-checkers-release', 302)


@app.route('/<path:path>')
def redirect_from_old_path(path):
    # DSL-ish
    url = None
    permanent = True

    # lab or specific redirect
    if any(path.startswith(prefix) for prefix in [
        'canvas-pong',
        'companion',
        'jquery-typing',
        'tmp',
    ]):
        url = 'http://lab.narf.pl/' + path
    else:
        url, permanent = {
            '/feed.xml': ('/feed', permanent),
            '/plain.txt': ('/posts/plain-text', permanent),
            '/quit.txt': ('/posts/quit-delicious', permanent),

            '/have-seen':
                (memoized.static_url_for_asset('index/urls/have-seen.jpg'),
                 not permanent),

            '/js':
                (memoized.static_url_for_asset('index/urls/ancient-aliens-javascript.jpg'),
                 not permanent),

            '/key':
                (memoized.static_url_for_asset('index/id_rsa.pub'),
                 not permanent),

            '/liczba':
                ('http://www.youtube.com/watch?v=Gc31UQ-C6dw',
                 not permanent),

            '/liczba-nie-ilosc':
                ('http://www.youtube.com/watch?v=Gc31UQ-C6dw',
                 not permanent),

            '/pie-chart':
                ('https://twitter.com/maxcroser/status/676563118512840704',
                 not permanent),

            '/samo-sie-nie-zrobi':
                ('http://www.youtube.com/watch?v=xOUjIr70XgQ',
                 not permanent),

            '/newsletter': ('http://eepurl.com/baKQjf', not permanent),
        }.get('/' + path, (None, None))

    # match latest post
    if not url:
        s = stupify(path)
        for post in memoized.public_posts():
            if s in post['stupified_title'] or \
               s in post['stupified_slug']:
                url = post['url']
                permanent = False
                break

    # 301, 302, or 404
    if url:
        return redirect(url, 301 if permanent else 302)
    else:
        return HTTP_404


if __name__ == '__main__':
    app.run(debug=True)
