from __future__ import absolute_import

import requests

from accountable.config import Config


class Resource(object):
    def __init__(self):
        self.config = Config()
        self.auth = self.config.auth
        self.api_uri = 'https://{}/rest/api/2'.format(self.config['domain'])

    def get(self, resource, params={}):
        r = requests.get('{}/{}'.format(self.api_uri, resource),
                         params=params,
                         auth=self.auth)
        return r.json()

    def post(self, resource, payload={}):
        r = requests.post('{}/{}'.format(self.api_uri, resource),
                          auth=self.auth,
                          json=payload)
        try:
            return r.json()
        except ValueError:
            return r
