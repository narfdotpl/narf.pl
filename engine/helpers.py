#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from functools import wraps
from hashlib import md5

from flask import redirect, request


class RouteFactory(object):
    """
    Example:

        route = RouteFactory(app)

        @route('/')
        def index():
            return 'hi'

    """

    def __init__(self, app):
        self.app = app

    def __call__(self, *args, **kwargs):
        return route(self.app, *args, **kwargs)


class route(object):
    """
    Decorator extending `app.route` with following functionality:

    - strip trailing slash
    - return 404 if function returns None
    """

    def __init__(self, app, *args, **kwargs):
        self._app = app
        self._route_args = args
        self._route_kwargs = kwargs

    def __call__(self, func):

        @self._app.route(*self._route_args, **self._route_kwargs)
        @wraps(func)
        def smart_func(*args, **kwargs):
            # strip trailing slash from path
            path = request.path
            if path != '/' and path.endswith('/'):
                return redirect(path.rstrip('/'), 301)

            # run func
            result = func(*args, **kwargs)

            # return result or 404
            if result is None:
                return '404', 404
            else:
                return result

        return smart_func


def get_hash(x):
    return md5(str(x)).hexdigest()
