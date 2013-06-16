#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from functools import wraps

from flask import current_app


class MetaMemoize(type):
    """
    Metaclass that applies `staticmethod` and `memoize` decorators to all
    its methods.
    """

    def __new__(cls, class_name, base_classes, attributes_dict):
        # go through class atributes
        for k, v in attributes_dict.iteritems():
            # skip magic attributes
            if k.startswith('__'):
                continue

            # decorate methods
            attributes_dict[k] = staticmethod(memoize(v))

        return type.__new__(cls, class_name, base_classes, attributes_dict)


def memoize(func):
    """
    Decorator for methods in the `Memoized` class.
    """

    @wraps(func)
    def smart_func(*args):
        # get or create dict for function results
        dct = func._mem_dict = getattr(func, '_mem_dict', {})

        # get memoized result or compute and memoize it
        key = args
        if key in dct and not current_app.debug:
            result = dct[key]
        else:
            result = func(*args)
            dct[key] = result

        return result

    return smart_func
