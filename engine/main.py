#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from collections import OrderedDict
from functools import partial, wraps
from hashlib import md5
from itertools import groupby
import json
from os import walk
from os.path import exists, join

import datetime
import re

try:
    import Image
except ImportError:
    from PIL import Image

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from flask import (Flask, Markup, make_response, redirect, render_template,
                   render_template_string, request)
from markdown import markdown as render_markdown
import typogrify.filters
import yaml

from memoize import MetaMemoize
import settings


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
        collections_by_id = {}
        posts = sorted(memoized.public_posts(), key=lambda x: x['date'])

        for post in posts:
            for id in post['collection_ids']:
                if id not in collections_by_id:
                    collections_by_id[id] = PostCollection(id)

                collections_by_id[id].posts.append(post)

        return collections_by_id.values()

    def draft_filenames():
        return filnames_in_directory(settings.DRAFTS_DIR)

    def is_draft(filename):
        return filename in memoized.draft_filenames()

    def is_hidden(filename):
        return memoized.is_draft(filename) or filename[:-len('.md')] in []

    def post_data(filename):
        # is post a draft?
        is_draft = memoized.is_draft(filename)
        title_prefix = 'DRAFT: ' if is_draft else ''
        directory = settings.DRAFTS_DIR if is_draft else settings.POSTS_DIR

        # get post split into sections
        separator = '\n\n'
        with open(join(directory, filename)) as f:
            sections = f.read().decode('utf8').split(separator)

        # parse YAML header
        header = Header(sections[0])

        # get data from sections
        slug = filename[:-len('.md')]
        title = title_prefix + sections[1].rstrip('=').rstrip('\n')
        path = ('/music/' if header.is_music_release else '/posts/') + slug

        return {
            'is_draft': is_draft,
            'is_hidden': memoized.is_hidden(filename),
            'date': header.date,
            'title': title,
            'stupified_title': stupify(title),
            'remaining_markdown': separator.join(sections[2:]),
            'slug': slug,
            'stupified_slug': stupify(slug),
            'path': path,
            'url': 'http://narf.pl%s' % path,
            'uses_black_css': header.theme == 'black',
            'collection_ids': header.collection_ids,
            'is_selected': header.is_selected,
            'music': header.music,
            'index_config': header.index_config,
        }

    def post_filenames():
        return filnames_in_directory(settings.POSTS_DIR)

    def public_posts():
        return antimap(memoized.post_filenames(), [
            partial(map, memoized.post_data),
            partial(filter, lambda x: not x['is_hidden']),
            partial(sorted, key=lambda x: x['date'], reverse=True),
        ])

    def feed_entries():
        # get entries from YAML
        path = join(settings.CONTENT_DIR, 'feed.yaml')
        with open(path) as f:
            entries = yaml.load(f)

        # add posts
        for post in memoized.public_posts():
            entries.append({
                'title': post['title'],
                'time': '%s 00:00' % post['date'],
                'link': post['url'],
            })

        # set "updated" field (ISO 8601) in a retarded manner
        for e in entries:
            e['updated'] = '%s:00+01:00' % e['time'].replace(' ', 'T')

        # sort entries by update time
        return sorted(entries, reverse=True, key=lambda e: e['updated'])

    def rendered_feed():
        return render_template('feed.xml', entries=memoized.feed_entries())

    def rendered_json_feed():
        # `OrderedDict` makes things quite ugly but the result is nicer...
        feed = OrderedDict([
            ('version', 'https://jsonfeed.org/version/1'),
            ('title', 'narf.pl'),
            ('home_page_url', 'http://narf.pl/'),
            ('feed_url', 'http://narf.pl/feed.json'),
            ('author', OrderedDict([
                ('name', 'Maciej Konieczny'),
                ('url', 'http://narf.pl/'),
            ])),
            ('items', [
                OrderedDict([
                    ('title', e['title']),
                    ('content_html', e.get('body') or 'visit <a href="{link}">{link}</a>'.format(**e)),
                    ('date_published', e['updated']),
                    ('url', e['link']),
                    ('id', e.get('uuid') or e['link']),
                ])
                for e in memoized.feed_entries()
            ]),
        ])

        return json.dumps(feed, indent=4)

    def rendered_404():
        html = render_template('404.html')
        html = resolve_asset_urls(html)

        return (html, 404)

    def index_entries():
        entries = []

        for post in memoized.public_posts():
            config = post['index_config']
            if config is None:
                continue

            image_url = None
            for filename in filter(None, [config.get('image'), 'index.jpg', 'index.png']):
                relative_path = post['slug'] + '/' + filename
                if relative_path in memoized.asset_relative_paths():
                    image_url = static_url.for_asset(relative_path)
                    break

            entries.append({
                'title': config.get('title', post['title']),
                'subtitle': config['subtitle'],
                'url': post['path'],
                'image': image_url,
                'sorting_key': config.get('sorting_key', post['date']),
                'post': post,
            })

        entries.append({
            'title': 'SwiftyStateMachine',
            'subtitle': u'µframework',
            'url': 'https://github.com/macoscope/SwiftyStateMachine',
            'image': static_url.for_asset('index/links/state-machine.png'),
            'sorting_key': '2015-03-23',
            'post': None,
        })

        date_to_str = lambda x: x.isoformat() if isinstance(x, datetime.date) else x
        entries = reversed(sorted(entries, key=lambda e: date_to_str(e['sorting_key'])))

        return entries

    def rendered_index():
        entries = memoized.index_entries()
        html = render_template('index.html', entries=entries)

        return antimap(html, [
            partial(resolve_local_urls, 'index.md'),  # dirty hack!  TODO: can we remove this?
            resolve_asset_urls,
        ])

    def rendered_post(filename):
        # get post data
        ctx = memoized.post_data(filename)
        ctx['youtube_iframe'] = make_youtube_iframe

        # render and process markdown
        ctx['content'] = antimap(ctx['remaining_markdown'], [
            lambda template: render_template_string(template, **ctx),
            render_markdown,
            wrap_images_in_figures_instead_of_paragraphs,
            center_figure_captions,
            turn_mp4_images_to_videos,
            partial(resolve_local_urls, filename),
            transform_image_lists_to_galleries,
            wrap_images_in_links,
            thumbnail_big_images,
            add_footnote_links,
            link_headers_and_render_table_of_contents,
            add_non_breaking_spaces,
        ])

        # add collections
        by_id = {c.id: c for c in memoized.collections()}
        ctx['collections'] = [by_id[id] for id in ctx['collection_ids']]

        # get dedicated social image
        social_image_url = None
        for extension in ['jpg', 'png']:
            relative_path = '%s/social.%s' % (filename[:-len('.md')],extension)
            if relative_path in memoized.asset_relative_paths():
                social_image_url = static_url.for_asset(relative_path)
                break

        # use first image as social image
        if social_image_url is None:
            soup = BeautifulSoup(ctx['content'])
            for img in soup.find_all('img'):
                social_image_url = img['src']
                break

        # set social image
        ctx['social_image_url'] = social_image_url

        # render final html
        html = render_template('post.html', **ctx)
        return antimap(html, [
            add_title_text_to_post_links,
            resolve_asset_urls,
        ])

    def rendered_posts():
        posts = memoized.public_posts()
        get_year = lambda post: year_filter(post['date'])
        html = render_template('posts.html',
            selected_posts=[p for p in posts if p['is_selected']],
            posts_by_year=groupby(posts, get_year),
        )

        return resolve_asset_urls(html)

    def rendered_music():
        section_titles = ['Releases', 'Soundtracks']
        sections = [{'title': title, 'entries': []} for title in section_titles]
        for section in sections:
            for entry in memoized.index_entries():
                music = (entry['post'] or {}).get('music')
                if music and music['section'] == section['title'].lower():
                    entry = entry.copy()
                    entry['subtitle'] = music.get('subtitle', entry['subtitle'])
                    section['entries'].append(entry)

        posts_in_sections = []
        for section in sections:
            for entry in section['entries']:
                posts_in_sections.append(entry['post'])

        all_posts = memoized.public_posts()
        other_music_posts = [
            p for p in all_posts
            if 'music and sound' in p['collection_ids']
            and p not in posts_in_sections
        ]

        html = render_template('music.html',
            sections=sections,
            other_posts=other_music_posts,
        )

        return resolve_asset_urls(html)


class static_url(object):

    @staticmethod
    def base():
        return '/static'

    @staticmethod
    def for_asset(path):
        # 'a/b/c' → '/static/assets/a/b/c?sdfsdfsdf'
        full_path = join(settings.ASSETS_DIR, path)
        base = static_url.base()
        return '%s/assets/%s?%s' % (base, path, get_file_hash(full_path))

    @staticmethod
    def for_thumbnail(path, max_width=1024*2, max_height=780*2):
        # 'a/b/c.jpg' → '/static/thumbnails/sdfsdfsdf.jpg'

        # get asset data
        asset_path = join(settings.ASSETS_DIR, path)
        image = Image.open(asset_path)
        width, height = image.size

        # don't scale small images
        if width <= max_width and height <= max_height:
            return static_url.for_asset(path)

        # create hashed filename
        asset_hash = get_file_hash(asset_path)
        filename = '%s.jpg' % get_hash('%s:%d:%d' % \
                                       (asset_hash, max_width, max_height))
        thumbnail_path = join(settings.THUMBNAILS_DIR, filename)
        url = '%s/thumbnails/%s' % (static_url.base(), filename)

        # create thumbnail if it doesn't exist
        if not exists(thumbnail_path):
            image.thumbnail((max_width, max_height), Image.ANTIALIAS)

            # deal with PNGs
            if image.mode != 'RGB':
                image = image.convert('RGB')

            image.save(thumbnail_path, "JPEG", quality=95)

        return url


class Header(object):
    def __init__(self, section):
        d = yaml.load(section)
        if not isinstance(d, dict):
            d = {'date': section}

        # the system so far was using date strings, so...
        date = d['date']
        if isinstance(date, datetime.date):
            date = date.isoformat()

        def change_ids(id):
            if id in ['music', 'sound']:
                return 'music and sound'
            else:
                return id

        self.date = date
        self.theme = d.get('theme', 'default')
        self.collection_ids = map(change_ids, d.get('collections', []))
        self.is_selected = d.get('is_selected', False)
        self.index_config = d.get('index')

        self.music = d.get('music')
        self.is_music_release = (self.music or {}).get('section') == 'releases'


class PostCollection(object):
    def __init__(self, id, name=None, posts=None):
        if name is None:
            words = id.split(' ')
            name = ' '.join([words[0].title()] + words[1:]) + ' series'

        self.id = id
        self.name = name
        self.posts = posts or []


def antimap(x, functions):
    """
    `antimap(x, [f, g])` == `g(f(x))`
    """

    for f in functions:
        x = f(x)

    return x


def soup_to_unicode(soup):
    return soup.encode('utf8', formatter='html').decode('utf8')


def soup(func):
    @wraps(func)
    def wrapper(html, *args, **kwargs):
        soup = BeautifulSoup(html)
        func(soup, *args, **kwargs)
        return soup_to_unicode(soup)

    return wrapper


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
        html = '<a name="footnotes"><hr/></a>'.join(html.rsplit('<hr/>', 1))

    return html


class patterns:
    os_x = re.compile(r'([\W^])OS X', re.UNICODE)
    single_character = re.compile(r"(([^'\w]|^)\w) (\w)", re.UNICODE)
    number_with_unit = re.compile(r'((\W|^)\d+(\.\d+)?) (\w)', re.UNICODE)
    version = re.compile(r'(\w) (\d+(\.\d+)*)', re.UNICODE)


def add_nbsp(s, nbsp='&nbsp;'):
    """
    >>> add_nbsp(u'on OS X, and')
    u'on OS&nbsp;X, and'

    >>> add_nbsp(u'''"I won't use Swift"''')
    u'"I&nbsp;won\\'t use Swift"'

    >>> add_nbsp(u'To do so, I created a play count graph')
    u'To do so, I&nbsp;created a&nbsp;play count graph'

    >>> add_nbsp(u'Quake 3')
    u'Quake&nbsp;3'

    >>> add_nbsp(u'only 8 GB of RAM')
    u'only&nbsp;8&nbsp;GB of RAM'

    >>> add_nbsp(u'took ~1.5 h and resulted in')
    u'took ~1.5&nbsp;h&nbsp;and resulted in'

    >>> add_nbsp(u'A B C D')
    u'A&nbsp;B&nbsp;C&nbsp;D'

    >>> add_nbsp(u'(A propos: iOS 9.3 will introduce a f.lux-like feature called Night Shift)')
    u'(A&nbsp;propos: iOS&nbsp;9.3&nbsp;will introduce a&nbsp;f.lux-like feature called Night Shift)'

    >>> add_nbsp(u'Logitech G400 mouse')
    u'Logitech G400 mouse'
    """

    # OS X as a special case
    s = patterns.os_x.sub(r'\1OS'+nbsp+r'X', s)

    # a single character should always be connected to the next word, e.g. "I am"
    # run multiple times to account for situations like "A B C D"
    while True:
        new_s = patterns.single_character.sub(r'\1'+nbsp+r'\3', s)
        if new_s == s:
            break
        else:
            s = new_s

    # number should be connected to the next word, e.g. "8 GB"
    s = patterns.number_with_unit.sub(r'\1'+nbsp+r'\4', s)

    # version should be connected to the previous word, e.g. "Quake 3"
    s = patterns.version.sub(r'\1'+nbsp+r'\2', s)

    return s


def add_non_breaking_spaces(html):
    soup = BeautifulSoup(html, 'html.parser')
    add_non_breaking_spaces_recursive(soup)

    return soup_to_unicode(soup)


def add_non_breaking_spaces_recursive(soup):
    if isinstance(soup, NavigableString):
        text = unicode(soup)
        new_text = add_nbsp(text, nbsp=u'\xa0')
        soup.replace_with(new_text)
    else:
        for element in soup.contents:
            add_non_breaking_spaces_recursive(element)


@soup
def add_title_text_to_post_links(soup):
    prefixes = [root + path
        for root in ['', 'http://narf.pl']
        for path in ['/posts', '/music']
    ]

    for link in soup.find_all('a'):
        url = link.get('href', '')

        if any(url.startswith(x) for x in prefixes):
            slug = url.split('/')[-1]

            for post in memoized.public_posts():
                if post['slug'] == slug:
                    link['title'] = post['title']
                    break


@soup
def center_figure_captions(soup):
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


@soup
def link_headers_and_render_table_of_contents(soup):
    headers = []  # `(title, id)` pairs

    for h2 in soup.find_all('h2'):
        # get title and id
        title = h2.text
        id = slugify(title)
        headers.append((title, id))

        # add link before header
        link = soup.new_tag('a', id=id)
        h2.insert_before(link)

    # render table of contents
    tag = soup.find('table-of-contents')
    if tag:
        p = tag.parent
        html = render_template('table-of-contents.html', headers=headers)
        p.replace_with(BeautifulSoup(html))


def get_hash(x):
    return md5(str(x)).hexdigest()


def get_file_hash(path):
    hasher = md5()

    with open(path, 'rb') as f:
        while True:
            data = f.read(128 * 1024)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()


def filnames_in_directory(directory):
    for root, dirnames, filenames in walk(directory):
        return [x for x in filenames if not x.startswith('.')]

    return []


def resolve_local_urls(filename, html):
    """
    >>> resolve_local_urls('foo.md', '<a href="bar.jpg">baz</a>')
    u'<a href="asset:foo/bar.jpg">baz</a>'
    """

    slug = filename[:-len('.md')]
    soup = BeautifulSoup(html)

    def change_url(tag, key):
        try:
            url = tag[key]
        except KeyError:
            return

        blacklist = ['/', '#', 'mailto:', settings.ASSET_PREFIX]
        if not ('//' in url or
                any(url.startswith(x) for x in blacklist)):
            tag[key] = '%s%s/%s' % (settings.ASSET_PREFIX, slug, url)

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


@soup
def resolve_asset_urls(soup):
    """
    >>> resolve_asset_urls('<img src="asset:index/css/naif.min.css"/>')
    u'<img src="/static/assets/index/css/naif.min.css?436df1d347d14cd4c259ed31eeced027"/>'
    """

    prefix = settings.ASSET_PREFIX

    for attr in ['href', 'src', 'content']:
        predicate = lambda tag: tag.has_attr(attr)
        for tag in soup.find_all(predicate):
            url = tag[attr]
            if url.startswith(prefix):
                path = url[len(prefix):]
                tag[attr] = static_url.for_asset(path)


slugify_regex = re.compile(r'[^\w-]')
hyphens_regex = re.compile(r'--+')

def slugify(s):
    """
    "Update • 2015-06-26" → "update-2015-06-26"
    """

    return hyphens_regex.sub('-',
        slugify_regex.sub('', s.lower().replace(' ', '-')))


stupify_regex = re.compile(r'[^a-z0-9]')

def stupify(s):
    """
    Transform string to lowercase and remove non-alphanumeric characters.
    """

    return stupify_regex.sub('', s.lower())


@soup
def thumbnail_big_images(soup):
    """
    >>> thumbnail_big_images('<img src="asset:solstice/9x16.jpg"/>')
    u'<img src="/static/thumbnails/6147dce0b47c1320b53744e890dd56b8.jpg"/>'
    """

    prefix = settings.ASSET_PREFIX

    for img in soup.find_all('img'):
        url = img['src']
        if url.startswith(prefix):
            path = url[len(prefix):]
            data = img.attrs.pop('data', None)
            kwargs = json.loads(data) if data else {}
            img['src'] = static_url.for_thumbnail(path, **kwargs)


@soup
def transform_image_lists_to_galleries(soup):
    for ul in soup.find_all('ul'):
        lis = ul.find_all('li')
        lis_children = [list(li.children) for li in lis]
        is_gallery = all(
            len(children) == 1 and children[0].name == 'img'
            for children in lis_children)

        if is_gallery:
            ul['class'] = 'gallery'
            for img in ul.find_all('img'):
                img['data'] = '{"max_width": %d}' % (375 * 2)


@soup
def turn_mp4_images_to_videos(soup):
    """
    >>> turn_mp4_images_to_videos('<img src="foo.mp4"/>')
    u'<video autoplay="autoplay" controls="controls" loop="loop" src="foo.mp4"></video>'
    """

    for img in soup.find_all('img'):
        src = img['src']
        if src.endswith('.mp4'):
            img.replace_with(soup.new_tag('video',
                src=src,
                controls='controls',
                autoplay='autoplay',
                loop='loop'))


@soup
def wrap_images_in_figures_instead_of_paragraphs(soup):
    """
    >>> wrap_images_in_figures_instead_of_paragraphs('<p><img src="foo.jpg"/></p>')
    u'<figure><img src="foo.jpg"/></figure>'
    """

    for img in soup.find_all('img'):
        # get parent paragraph
        parent = img.parent
        if parent and parent.name == 'a':
            parent = parent.parent

        # change <p> into <figure>
        if parent and parent.name == 'p':
            parent.name = 'figure'


@soup
def wrap_images_in_links(soup):
    """
    >>> wrap_images_in_links('<img src="foo.jpg"/>')
    u'<a href="foo.jpg"><img src="foo.jpg"/></a>'
    """

    for img in soup.find_all('img'):
        if not (img.parent and img.parent.name == 'a'):
            a = soup.new_tag('a')
            a['href'] = img['src']
            a.append(img.replace_with(a))


def make_youtube_iframe(video_id):
    return Markup("""
<figure>
    <div class="video-wrapper">
        <iframe src="//www.youtube-nocookie.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
    </div>
</figure>
"""[1:-1].format(video_id=video_id))


@app.template_filter('typo')
def typo_filter(text):
    text = typogrify.filters.widont(text)
    text = typogrify.filters.smartypants(text)
    text = text.replace('OS X', 'OS&nbsp;X')

    return Markup(text)


@app.template_filter('year')
def year_filter(text):
    """
    >>> year_filter('2022-01-08')
    '2022'
    """

    return text.split('-')[0]


@app.before_request
def strip_trailing_slash():
    path = request.path
    if path != '/' and path.endswith('/'):
        return redirect(path.rstrip('/'), 301)


@app.route('/')
def index():
    return memoized.rendered_index()


@app.route('/music')
def music():
    return memoized.rendered_music()


@app.route('/posts')
def posts():
    return memoized.rendered_posts()


@app.route('/<any(posts, music):container>/<path:slug>')
def post(container, slug):
    if slug == 'spaghetti-trees':
        return redirect('/posts/metal-trees', 301)

    path = '/' + container + '/' + slug
    filename = slug + '.md'

    if filename in memoized.post_filenames():
        # redirect to proper container
        post = memoized.post_data(filename)
        expected_path = post['path']
        if path != expected_path:
            return redirect(expected_path)
        else:
            return memoized.rendered_post(filename)
    else:
        return memoized.rendered_404()


@app.route('/drafts/<path:slug>')
def draft(slug):
    filename = slug + '.md'
    if filename in memoized.post_filenames():
        return redirect(memoized.post_data(filename)['path'])
    elif filename in memoized.draft_filenames():
        return memoized.rendered_post(filename)
    else:
        return memoized.rendered_404()


@app.route('/feed')
def feed():
    response = make_response(memoized.rendered_feed())
    response.mimetype = 'application/atom+xml'
    return response


@app.route('/feed.json')
def feed_json():
    response = make_response(memoized.rendered_json_feed())
    response.mimetype = 'application/json'
    return response


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
        suspense = static_url.for_asset('5k-imac/suspense_accent_1.mp3')
        url, permanent = {
            '/feed.xml': ('/feed', permanent),
            '/plain.txt': ('/posts/plain-text', permanent),
            '/quit.txt': ('/posts/quit-delicious', permanent),

            '/cv': ('https://www.linkedin.com/in/narfdotpl', not permanent),
            '/blog': ('/posts', not permanent),
            '/checkers': ('/posts/checkers-presskit', not permanent),

            '/have-seen':
                (static_url.for_asset('index/urls/have-seen.jpg'),
                 not permanent),

            '/js':
                (static_url.for_asset('index/urls/ancient-aliens-javascript.jpg'),
                 not permanent),

            '/now': ('/posts/anxious-timer', not permanent),

            '/suspense': (suspense, not permanent),
            '/suspens':  (suspense, not permanent),

            '/newsletter': ('http://eepurl.com/baKQjf', not permanent),
            '/nf1': ('/posts/its-alive', not permanent),
            '/cringe': ('https://www.youtube.com/watch?v=hk3Qh8O1pb8', not permanent),
            '/nft': ('/posts/optimism', not permanent),
            '/1d': ('https://monthly.com/p/xPzL6t', not permanent),
            '/ld': ('https://monthly.com/p/xPzL6t', not permanent),
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
        return memoized.rendered_404()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    app.run(debug=True, host='0.0.0.0')
