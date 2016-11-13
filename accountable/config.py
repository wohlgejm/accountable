import os
from operator import itemgetter

import click
import yaml

from requests.auth import HTTPBasicAuth


class Config(object):
    CONFIG_DIR = os.path.expanduser('~/.accountable')
    CONFIG_FILE = '{}/config.yaml'.format(CONFIG_DIR)
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

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._config = None
        self.username, self.password, self.domain, self.issue_fields = \
            itemgetter(
                'username', 'password', 'domain', 'issue_fields'
            )(self.config)
        self.auth = HTTPBasicAuth(self.username, self.password)

    @property
    def config(self):
        if self.kwargs.get('create_config'):
            self._initial_setup(self.kwargs)
        self._config = self._load_config()
        return self._config

    def _load_config(self):
        with open(self.CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
        return config

    def _initial_setup(self, kwargs):
        username = str(kwargs.get('username'))
        password = str(kwargs.get('password'))
        domain = str(kwargs.get('domain'))
        config_dict = self._config_dict(username, password, domain)
        self._create_config(config_dict)

    def _create_config_dir(self):
        if not os.path.exists(self.CONFIG_DIR):
            click.echo('Creating {}'.format(self.CONFIG_DIR))
            os.makedirs(self.CONFIG_DIR)

    def _config_dict(self, username, password, domain):
        config = {
            'username': username,
            'password': password,
            'domain': domain,
            'issue_fields': self.DEFAULT_ISSUE_FIELDS,
            'aliases': self.DEFAULT_ALIASES
        }
        return config

    def _create_config(self, config_dict):
        self._create_config_dir()
        with open(self.CONFIG_FILE, 'w+') as f:
            f.write(yaml.dump(config_dict, default_flow_style=False))
        click.echo('Configuration file written to {}'.format(self.CONFIG_FILE))
