from __future__ import absolute_import

from collections import OrderedDict

from accountable.jira import Jira
from accountable.config import Config


class Accountable(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.config = Config(kwargs)
        else:
            self.config = Config()
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
        data['Reporter'] = fields['reporter']['displayName']
        data['Assignee'] = fields['assignee']['displayName']
        data['Issue Type'] = fields['issuetype']['name']
        data['Status'] = fields['status']['statusCategory']['name']
        data['Priority'] = fields['priority']['name']
        data['Summary'] = fields['summary']
        data['Description'] = fields['description']
        return data
