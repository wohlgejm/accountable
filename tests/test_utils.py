from __future__ import absolute_import

from collections import OrderedDict

from accountable.utils import reshape, nargs_to_dict


def test_nargs_to_dict():
    options = (
        'project.id', '11900', 'issuetype.id', '7',
        'summary', 'a summary'
    )
    assert nargs_to_dict(options) == {
        'fields': {
            'project': {
                'id': 11900
            },
            'issuetype': {
                'id': 7
            },
            'summary': 'a summary'
        }
    }


def test_nargs_to_dict_eval():
    options = (
        'project.id', '11900',
        'issuetype.id', '7',
        'summary', 'a summary',
        'labels', '["engineering"]'
    )
    assert nargs_to_dict(options) == {
        'fields': {
            'project': {
                'id': 11900
            },
            'issuetype': {
                'id': 7
            },
            'summary': 'a summary',
            'labels': ['engineering']
        }
    }


def test_reshape():
    schema = {'one': {'two': 'three'}}
    data = {'one': {'two': {'three': 'value'},
                    'garbage': {'garbage': 1}}}
    assert reshape(schema, data) == OrderedDict({
        'one': {'two': {'three': 'value'}}
    })


def test_reshape_nested_list():
    schema = {'keepme': ['keepme', 'andme']}
    data = {'keepme': [{'keepme': 'value', 'andme': 'value', 'nope': 'nope'}]}
    assert reshape(schema, data) == OrderedDict({
        'keepme': [{'keepme': 'value'}]
    })


def test_reshape_list():
    schema = [{'one': [{'two': 'three'}]}]
    data = [{'one': [{'two': {'three': 'value', 'nope': 'nope'}}]}]

    assert reshape(schema, data) == [{
        'one': [{'two': {'three': 'value'}}]
    }]


def test_reshape_none_value():
    schema = {'one': None}
    data = {'one': 'value', 'other': 'value2'}

    assert reshape(schema, data) == OrderedDict({'one': 'value'})
