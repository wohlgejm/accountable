from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from collections import MutableSequence, MutableMapping
except ImportError:
    from collections.abc import MutableSequence, MutableMapping
from collections import OrderedDict
import ast


def reshape(schema, data):
    reshaped = [] if isinstance(schema, MutableSequence) else OrderedDict()

    def _reshape(schema, data, new_data):
        if isinstance(schema, MutableMapping):
            for idx, (key, value) in enumerate(schema.items()):
                try:
                    d = data[key]
                except KeyError:
                    continue
                new_data[key] = (
                    [] if isinstance(value, MutableSequence) else {}
                )
                if not value:
                    new_data[key] = data[key]
                else:
                    _reshape(value, d, new_data[key])
        elif isinstance(schema, MutableSequence):
            schema = schema[0]
            for idx, datum in enumerate(data):
                try:
                    new_data[idx]
                except IndexError:
                    new_data.append({})
                _reshape(schema, datum, new_data[idx])
        else:
            new_data[schema] = data[schema]
    _reshape(schema, data, reshaped)
    return reshaped


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


def flatten(d, parent_key='', sep='-'):
    items = []
    for k, v in d.items():
        new_key = (parent_key + sep + k if parent_key else k).upper()
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return OrderedDict(sorted(items))
