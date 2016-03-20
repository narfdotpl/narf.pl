#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division


class PostCollection(object):

    def __init__(self, tagline, posts):
        self.tagline = tagline
        self.posts = posts

        padded_posts = [None] + posts + [None]
        for (i, post) in enumerate(padded_posts):
            if post:
                post['collection_navigation_item'] = \
                    PostCollectionNavigationItem(self, padded_posts[i - 1],
                                                       padded_posts[i + 1])


class PostCollectionNavigationItem(object):

    def __init__(self, collection, previous_post, next_post):
        self.collection = collection
        self.previous_post = previous_post
        self.next_post = next_post

    @property
    def tagline(self):
        return self.collection.tagline


def add_collections_to_posts(posts):
    # yay for mutable data! :E

    posts_in_original_order = posts
    posts = sorted(posts, key=lambda x: x['date'])

    # max one collection per post, last one wins
    PostCollection("Checkers series",
                   filter(lambda x: 'checkers' in x['slug'], posts))
    PostCollection("Setup series",
                   filter(lambda x: x['slug'] in [
                       'menu-bar',
                       '5k-imac',
                       'mac-software',
                   ], posts))
    PostCollection("Procedural series",
                   filter(lambda x: x['slug'] in [
                       'shattered-polygons',
                       'sketchy-procedures',
                   ], posts))

    return posts_in_original_order
