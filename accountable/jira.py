import requests
from requests.auth import HTTPBasicAuth


class Jira(object):
    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain
        self.auth = HTTPBasicAuth(self.username, self.password)

    @property
    def endpoint(self):
        return 'https://{}/rest/api/2'.format(self.domain)

    @property
    def metadata_endpoint(self):
        return '{}/issue/createmeta'.format(self.endpoint)

    @property
    def issue_endpoint(self, issue_key):
        return '{}/issue/{}/worklog'.format(self.endpoint, issue_key)

    def metadata(self):
        r = requests.get(self.metadata_endpoint,
                         auth=self.auth)
        return r.json()


class Issue(Jira):
    def __init__(self, issue_key, username, password, domain):
        self.issue_key = issue_key
        super(Issue, self).__init__(username, password, domain)

    def worklog(self):
        r = requests.get(self.issue_endpoint,
                         auth=self.auth)
        return r.json

    def transitions(self):
        return

    @property
    def issue_endpoint(self):
        return '{}/issue/{}/worklog'.format(self.endpoint, self.issue_key)
