#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from hashlib import md5
from os import walk
from os.path import getmtime, join

from flask import Flask, redirect, request
from jinja2 import Template
from markdown import markdown as render_markdown

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

    def html_for_filename(filename):
        with open(join(settings.TEMPLATES_DIR, filename)) as f:
            return f.read()

    def post_filenames():
        for root, dirnames, filenames in walk(settings.POSTS_DIR):
            return [x for x in filenames if not x.startswith('.')]

    def post_template():
        with open(join(settings.TEMPLATES_DIR, 'post.html')) as f:
            return Template(f.read())

    def rendered_post(filename):
        # get post split into sections
        separator = '\n\n'
        with open(join(settings.POSTS_DIR, filename)) as f:
            sections = f.read().split(separator)

        # get data from sections
        date = sections[0]
        title = sections[1].rstrip('=').rstrip('\n')
        remaining_markdown = separator.join(sections[2:])

        # render html
        html = render_markdown(remaining_markdown)
        return memoized.post_template().render(title=title, date=date,
                                               content=html)
    def static_url_for_asset(path):
        # 'a/b/c' → '/static/assets/a/b/c?sdfsdfsdf'
        mtime = getmtime(join(settings.ASSETS_DIR, path))
        return '/static/assets/%s?%s' % (path, get_hash(mtime))


def get_hash(x):
    return md5(str(x)).hexdigest()


@app.before_request
def strip_trailing_slash():
    path = request.path
    if path != '/' and path.endswith('/'):
        return redirect(path.rstrip('/'), 301)


@app.route('/')
def index():
    return memoized.html_for_filename('index.html')


@app.route('/posts')
def posts():
    return memoized.html_for_filename('posts.html')


@app.route('/posts/<path:slug>')
def post(slug):
    filename = slug + '.md'
    if filename in memoized.post_filenames():
        return memoized.rendered_post(filename)
    else:
        return HTTP_404


@app.route('/assets/<path:path>')
def asset(path):
    if path in memoized.asset_relative_paths():
        return redirect(memoized.static_url_for_asset(path))
    else:
        return HTTP_404


if __name__ == '__main__':
    app.run(debug=True)
