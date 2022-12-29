#!/usr/bin/env python
# encoding: utf-8

from functools import wraps

from flask import current_app


class MetaMemoize(type):
    """
    Metaclass that applies `staticmethod` and `memoize` decorators to all
    its methods.
    """

    def __new__(cls, class_name, base_classes, attributes_dict):
        # go through class atributes
        for k, v in attributes_dict.items():
            # skip magic attributes
            if k.startswith('__'):
                continue

            # decorate methods
            attributes_dict[k] = staticmethod(memoize(v))

        return type.__new__(cls, class_name, base_classes, attributes_dict)


def is_debug():
    """
    Returns `True` if debug mode is on.
    """
    try:
        return current_app.debug
    except RuntimeError:
        return True


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
        if key in dct and not is_debug():
            result = dct[key]
        else:
            result = func(*args)
            dct[key] = result

        return result

    return smart_func
