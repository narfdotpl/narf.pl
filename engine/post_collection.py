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

    def navigation_item_for_post(self, post):
        if not self.contains_post(post):
            return None

        padded_posts = [None] + self.posts + [None]
        for (i, p) in enumerate(padded_posts):
            if p and p['slug'] == post['slug']:
                return PostCollectionNavigationItem(self.tagline,
                                                    padded_posts[i - 1],
                                                    padded_posts[i + 1])


class PostCollectionNavigationItem(object):

    def __init__(self, tagline, previous_post, next_post):
        self.tagline = tagline
        self.previous_post = previous_post
        self.next_post = next_post
