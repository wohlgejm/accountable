from __future__ import absolute_import

try:
    from collections import MutableSequence
except ImportError:
    from collections.abc import MutableSequence
import ast


def nargs_to_dict(nargs):
    d = {}
    for arg in zip(nargs[0::2], nargs[1::2]):
        key, value = arg
        parsed_value = eval_value(value)
        rec_nargs_to_dict(key, parsed_value, d)
    return {'fields': d}


def rec_nargs_to_dict(key, value, d):
    if isinstance(key, MutableSequence):
        keys = key.split('.')
        head, tail = keys[0], keys[1:]
        if not d.get(head):
            d[head] = {}
        rec_nargs_to_dict(tail, value, d[head])
    d[key] = value
    return d


def eval_value(value):
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
