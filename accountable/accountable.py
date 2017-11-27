from __future__ import absolute_import

import os
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from git import Repo
from slugify import slugify

from accountable.config import Config
from accountable.resource import Resource
from accountable.utils import nargs_to_dict, reshape, flatten


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
        data = self.issue()
        return flatten(
            reshape({'fields': Config().issue_schema()}, data)['fields']
        )

    def issue_create(self, options):
        payload = nargs_to_dict(options)
        return self.resource.post('issue', payload)

    def create_meta(self, project_key, issue_type):
        params = {
            'expand': 'projects.issuetypes.fields',
            'projectKeys': project_key,
            'issuetypeNames': issue_type
        }
        params = dict((k, v) for k, v in params.iteritems() if v)
        root = 'issue/createmeta'
        metadata = self.resource.get(
            '{}?{}'.format(
                root,
                urlencode(params)
            )
        ).get('projects')
        return [flatten(p) for p in metadata]

    def checkout_branch(self, options):
        payload = nargs_to_dict(options)
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
        payload = nargs_to_dict(options)
        self.resource.put('issue/{}'.format(self.issue_key),
                          payload)
        return self.issue_meta()

    def issue_comments(self):
        comments = self.resource.get('issue/{}/comment'.format(self.issue_key))
        if comments.get('comments'):
            return [flatten(comment) for comment in comments['comments']]
        return None

    def issue_add_comment(self, body):
        comment = self.resource.post(
            'issue/{}/comment'.format(self.issue_key),
            {'body': body}
        )
        return flatten(comment)

    def issue_worklog(self):
        worklog = self.resource.get('issue/{}/worklog'.format(self.issue_key))
        if worklog.get('worklogs'):
            return [flatten(w) for w in worklog.get('worklogs')]
        return None

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
        if payload:
            return [flatten(user) for user in payload]
        return None

    def _repo(self):
        return Repo(os.getcwd()).git
