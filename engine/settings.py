#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os.path import dirname, join, realpath


_current_dir = dirname(realpath(__file__))
REPO_DIR = join(_current_dir, '..')
CONTENT_DIR = join(REPO_DIR, 'content')
ASSETS_DIR = join(CONTENT_DIR, 'assets')
TEMPLATES_DIR = join(CONTENT_DIR, 'templates')
POSTS_DIR = join(CONTENT_DIR, 'posts')
