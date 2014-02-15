#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import datetime
from functools import partial
from hashlib import md5
from os import walk
from os.path import exists, getmtime, join
import re

import Image
from bs4 import BeautifulSoup
from flask import (Flask, Markup, make_response, redirect, render_template,
    request)
from markdown import markdown as render_markdown
import typogrify.filters
import yaml

from memoize import MetaMemoize
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

    def post_filenames():
        for root, dirnames, filenames in walk(settings.POSTS_DIR):
            return [x for x in filenames if not x.startswith('.')]

    def rendered_feed():
        # get entries from YAML
        path = join(settings.CONTENT_DIR, 'feed.yaml')
        with open(path) as f:
            entries = yaml.load(f)

        # add posts
        for filename in memoized.post_filenames():
            dct = get_post_data(filename)
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
        return render_template('index.html', year=datetime.date.today().year)

    def rendered_post(filename):
        # get post data
        ctx = get_post_data(filename)

        # render and process markdown
        ctx['content'] = antimap(ctx['remaining_markdown'], [
            render_markdown,
            partial(resolve_asset_urls, filename),
            wrap_images_in_figures_instead_of_paragraphs,
            wrap_images_in_links,
            thumbnail_big_images,
            add_footnote_links,
        ])

        # get image URLs
        soup = BeautifulSoup(ctx['content'])
        ctx['image_urls'] = []
        for img in soup.find_all('img'):
            url = img['src']

            # add domain
            if url.startswith('/'):
                url = 'http://narf.pl' + url

            ctx['image_urls'].append(url)


        # render final html
        return render_template('post.html', **ctx)

    def rendered_posts():
        posts = sorted(map(get_post_data, memoized.post_filenames()),
                       key=lambda dct: dct['date'], reverse=True)

        return render_template('posts.html', posts=posts)

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

        # don't scale small images
        max_width = 1024
        max_height = 780
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


def get_hash(x):
    return md5(str(x)).hexdigest()


def get_post_data(filename):
    # get post split into sections
    separator = '\n\n'
    with open(join(settings.POSTS_DIR, filename)) as f:
        sections = f.read().decode('utf8').split(separator)

    # get data from sections
    slug = filename[:-len('.md')]
    return {
        'date': sections[0],
        'title': sections[1].rstrip('=').rstrip('\n'),
        'remaining_markdown': separator.join(sections[2:]),
        'slug': slug,
        'url': 'http://narf.pl/posts/%s' % slug,
    }


def resolve_asset_urls(filename, html):
    """
    >>> resolve_asset_urls('foo.md', '<a href="bar.jpg">baz</a>')
    u'<a href="/assets/foo/bar.jpg">baz</a>'
    """

    slug = filename[:-len('.md')]
    soup = BeautifulSoup(html)

    def change_url(tag, key):
        url = tag[key]
        if not (url.startswith('/') or url.startswith('#') or '//' in url):
            tag[key] = '/assets/%s/%s' % (slug, url)

    for tag_name, key in [
        ('a', 'href'),
        ('img', 'src'),
    ]:
        for tag in soup.find_all(tag_name):
            change_url(tag, key)

    return unicode(soup)


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


@app.route('/key')
def redirect_to_key():
    return redirect(memoized.static_url_for_asset('index/id_rsa.pub'))


@app.route('/companion')
def redirect_to_companion():
    # save stats
    path = join(settings.STATS_DIR, 'companion.csv')
    with open(path, 'a') as f:
        f.write('%s\t%s\t%s\n' % (
            datetime.datetime.now().isoformat(),
            request.url,
            request.headers.get('Referer')))

    return redirect('http://lab.narf.pl/companion/')


SPECIFIC_REDIRECTS = {
    '/feed.xml': '/feed',
    '/plain.txt': '/posts/plain-text',
    '/quit.txt': '/posts/quit-delicious',
    '/samo-sie-nie-zrobi': 'http://www.youtube.com/watch?v=xOUjIr70XgQ',
}
LAB_REDIRECT_PREFIXES = ['canvas-pong', 'jquery-typing', 'tmp']

@app.route('/<path:path>')
def redirect_from_old_path(path):
    # lab or specific redirect
    if any(path.startswith(prefix) for prefix in LAB_REDIRECT_PREFIXES):
        url = 'http://lab.narf.pl/' + path
    else:
        url = SPECIFIC_REDIRECTS.get('/' + path, None)

    # 301 or 404
    if url:
        return redirect(url, 301)
    else:
        return HTTP_404


if __name__ == '__main__':
    app.run(debug=True)
