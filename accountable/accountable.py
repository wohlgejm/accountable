from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import os

from git import Repo
from slugify import slugify

from accountable.config import Config
from accountable.resource import Resource


class Accountable(object):
    def __init__(self):
        self.issue_key = None

    @property
    def resource(self):
        return Resource()

    def issue_types(self, project_key):
        metadata = self.metadata()
        if project_key:
            project = next(
                project for project in metadata['projects']
                if project['key'] == str(project_key)
            )
            return {project_key: project['issuetypes']}
        else:
            issue_types = {}
            for project in metadata['projects']:
                issue_types[project['key']] = project['issuetypes']
            return issue_types

    def metadata(self):
        return self.resource.get('issue/createmeta')

    def issue(self):
        return self.resource.get('issue/{}'.format(self.issue_key))

    def issue_meta(self):
        fields = self.issue()['fields']

        data = OrderedDict()
        for field in Config()['issue_fields']:
            field_name = self._field_name(field)
            data[field_name] = self._access_field(field, fields)
        return data

    def issue_create(self, options):
        payload = Nargs(options).__dict__()
        return self.resource.post('issue', payload)

    def checkout_branch(self, options):
        payload = Nargs(options).__dict__()
        new_issue = self.issue_create(options)
        summary = payload['fields']['summary']
        key = new_issue['key']
        self._repo().checkout('HEAD', b='{}-{}'.format(key, slugify(summary)))
        return new_issue

    def checkout(self, issue_key):
        self.issue_key = issue_key
        issue = self.issue()
        issue_data = {
            'self': issue['self'],
            'id': issue['id'],
            'key': issue['key']
        }
        branch_name = '{}-{}'.format(issue_key, slugify(
            issue['fields']['summary'])
        )

        self._repo().branch('-f', branch_name)
        self._repo().checkout(branch_name)
        return issue_data

    def project_components(self, project_key):
        return self.resource.get('project/{}/components'.format(project_key))

    def issue_update(self, options):
        payload = Nargs(options).__dict__()
        self.resource.put('issue/{}'.format(self.issue_key),
                          payload)
        return self.issue_meta()

    def issue_comments(self):
        return self.resource.get('issue/{}/comment'.format(self.issue_key))

    def issue_add_comment(self, body):
        return self.resource.post('issue/{}/comment'.format(self.issue_key),
                                  {'body': body})

    def issue_worklog(self):
        return self.resource.get('issue/{}/worklog'.format(self.issue_key))

    def issue_transitions(self):
        return self.resource.get(
            'issue/{}/transitions'.format(self.issue_key)
        )

    def issue_do_transition(self, transition_id):
        return self.resource.post(
            'issue/{}/transitions'.format(self.issue_key),
            {'transition': {'id': transition_id}}
        )

    def users(self, query):
        payload = self.resource.get('user/search',
                                    params={'username': query})
        return payload

    def _repo(self):
        return Repo(os.getcwd()).git

    @staticmethod
    def _access_field(field, d):
        if isinstance(field, str):
            return d[field]
        elif isinstance(field, dict):
            value = d[list(field.keys())[0]]
            return Accountable._access_field(list(field.values())[0], value)
        else:
            raise TypeError('There is an issue with your issue field'
                            'configuration.')

    @staticmethod
    def _field_name(field):
        if isinstance(field, str):
            return field.upper()
        else:
            return list(field.keys())[0].upper()


class Nargs(object):
    def __init__(self, options):
        self._dict = self._args_to_dict(options)

    def __repr__(self):
        return repr(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

    def __dict__(self):
        return self._dict

    def _args_to_dict(self, args_tuple):
        d = {}
        for arg in zip(args_tuple[0::2], args_tuple[1::2]):
            keys = arg[0].split('.')
            self._set_nested_key(keys, arg[1], d)
        return {'fields': d}

    def _set_nested_key(self, key, value, d):
        if isinstance(key, list) and len(key) > 1:
            head, tail = key[0], key[1:]
            if not d.get(head):
                d[head] = {}
            self._set_nested_key(tail, value, d[head])
        else:
            d[list(key)[0]] = value
        return d
