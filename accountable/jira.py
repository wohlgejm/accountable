import requests
from requests.auth import HTTPBasicAuth


class Jira(object):
    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain

    @property
    def endpoint(self):
        return 'https://{}/rest/api/2'.format(self.domain)

    @property
    def metadata_endpoint(self):
        return '{}/issue/createmeta'.format(self.endpoint)

    def metadata(self):
        r = requests.get(self.metadata_endpoint,
                         auth=HTTPBasicAuth(self.username, self.password))
        return r.json()
