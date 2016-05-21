from __future__ import unicode_literals

import requests


class Jira(object):
    def __init__(self, domain, auth):
        self.domain = domain
        self.auth = auth
        self.endpoint = 'https://{}/rest/api/2'.format(self.domain)

    @property
    def issue_endpoint(self, issue_key):
        return '{}/issue/{}/worklog'.format(self.endpoint, issue_key)

    def metadata(self):
        return Resource(self, 'issue/createmeta', 'get').response()

    def issue(self, issue_key):
        return Resource(self, 'issue/{}'.format(issue_key), 'get').response()

    def issue_comments(self, issue_key):
        return Resource(self, 'issue/{}/comment'.format(issue_key),
                        'get').response()


class Resource(object):
    def __init__(self, jira, resource_name, method):
        self.resource_endpoint = '{}/{}'.format(jira.endpoint, resource_name)
        self.auth = jira.auth
        self.method = method

    def response(self):
        method = self.method.lower()
        if method == 'get':
            return self.get()
        elif method == 'post':
            return self.post()
        else:
            raise NotImplementedError

    def get(self):
        r = requests.get(self.resource_endpoint, auth=self.auth)
        return r.json()

    def post():
        pass
