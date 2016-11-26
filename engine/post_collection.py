#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division


class PostCollectionRecipe(object):

    def __init__(self, tagline, predicate=None, slugs=None):
        self.tagline = tagline

        if slugs:
            self.predicate = lambda post: post['slug'] in slugs
        else:
            self.predicate = predicate

    def collection_with_posts(self, posts):
        return PostCollection(self.tagline, filter(self.predicate, posts))


class PostCollection(object):

    def __init__(self, tagline, posts):
        self.tagline = tagline
        self.posts = posts

    def contains_post(self, post):
        return post['slug'] in [p['slug'] for p in self.posts]
