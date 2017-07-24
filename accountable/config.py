import os
try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

import click
import yaml

from requests.auth import HTTPBasicAuth


CONFIG_DIR = os.path.expanduser('~/.accountable')
DEFAULT_ISSUE_FIELDS = [
    {'reporter': 'displayName'},
    {'assignee': 'displayName'},
    {'issuetype': 'name'},
    {'status': {'statusCategory': 'name'}},
    'summary',
    'description'
]
DEFAULT_ALIASES = {'cob': 'checkoutbranch',
                   'co': 'checkout'}
CONFIG_FILE = '{}/config.yaml'.format(CONFIG_DIR)


class Config(UserDict, object):
    def __getitem__(self, key):
        if not self.data:
            self.data = self._load_config()
        return self.data[key]

    def update(self, *args, **kwargs):
        if self._exists():
            self.data = self._load_config()
        super(Config, self).update(*args, **kwargs)
        self.data.setdefault('aliases', DEFAULT_ALIASES)
        self.data.setdefault('issue_fields', DEFAULT_ISSUE_FIELDS)
        self._save()

    @property
    def auth(self):
        return HTTPBasicAuth(self['username'], self['password'])

    def _exists(self):
        return True if os.path.isfile(CONFIG_FILE) else False

    def _load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
        return config

    def _save(self):
        self._create_config_dir()
        with open(CONFIG_FILE, 'w+') as f:
            f.write(yaml.dump(self.data, default_flow_style=False,
                              encoding='utf-8'))
        click.secho(
            'Configuration file written to {}'.format(CONFIG_FILE),
            fg='blue'
        )

    def _create_config_dir(self):
        if not os.path.exists(CONFIG_DIR):
            click.secho('Creating {}'.format(CONFIG_DIR), fg='blue')
            os.makedirs(CONFIG_DIR)
