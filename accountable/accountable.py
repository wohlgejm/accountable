from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict

from accountable.jira import Jira
from accountable.config import Config


class Accountable(object):
    def __init__(self, **kwargs):
        self.config = Config(**kwargs)
        self.client = Jira(self.config.domain, self.config.auth)

    def _metadata(self):
        metadata = self.client.metadata()
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
        fields = self.client.issue(issue_key)['fields']
        data = OrderedDict()
        for field in self.config.issue_fields:
            field_name = self._field_name(field)
            data[field_name] = self._access_field(field, fields)
        return data

    def issue_comments(self, issue_key):
        return self.client.issue_comments(issue_key)['comments']

    @staticmethod
    def _access_field(field, d):
        if isinstance(field, str):
            return d[field]
        elif isinstance(field, dict):
            value = d[field.keys()[0]]
            return Accountable._access_field(field.values()[0], value)
        else:
            raise TypeError('There is an issue with your issue field'
                            'configuration.')

    @staticmethod
    def _field_name(field):
        if isinstance(field, str):
            return field.upper()
        else:
            return field.keys()[0].upper()
