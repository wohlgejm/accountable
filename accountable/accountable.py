from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict

import requests

from accountable.config import Config


class Accountable(object):
    def __init__(self, **kwargs):
        self.config = Config(**kwargs)
        self.resource = Resource(self.config.auth)
        self.api_uri = 'https://{}/rest/api/2'.format(self.config.domain)

    def _metadata(self):
        metadata = self.resource.get('{}/issue/createmeta'
                                     .format(self.api_uri))
        return metadata

    def projects(self):
        metadata = self._metadata()
        return [(project['key'],
                 project['name']) for project in metadata['projects']]

    def issue_types(self, project_key):
        metadata = self._metadata()
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

    def issue_meta(self, issue_key):
        fields = self.resource.get('{}/issue/{}'.format(self.api_uri,
                                                        issue_key))['fields']
        data = OrderedDict()
        for field in self.config.issue_fields:
            field_name = self._field_name(field)
            data[field_name] = self._access_field(field, fields)
        return data

    def issue_comments(self, issue_key):
        return self.resource.get('{}/issue/{}/comment'.format(self.api_uri,
                                                              issue_key))

    def issue_add_comment(self, issue_key, body):
        return self.resource.post('{}/issue/{}/comment'
                                  .format(self.api_uri, issue_key),
                                  {'body': body})

    def issue_worklog(self, issue_key):
        return self.resource.get('{}/issue/{}/worklog'.format(self.api_uri,
                                                              issue_key))

    def issue_transitions(self, issue_key):
        return self.resource.get(
            '{}/issue/{}/transitions'.format(self.api_uri, issue_key)
        )

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


class Resource(object):
    def __init__(self, auth):
        self.auth = auth

    def get(self, endpoint):
        r = requests.get(endpoint, auth=self.auth)
        return r.json()

    def post(self, endpoint, payload={}):
        r = requests.post(endpoint, auth=self.auth,
                          json=self.payload)
        return r.json()
