import os

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

    def __init__(self, **kwargs):
        if kwargs.get('create_config'):
            self._initial_setup(kwargs)
        self.config = self._load_config()
        self.username = self.config['username']
        self.password = self.config['password']
        self.domain = self.config['domain']
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.issue_fields = self.config['issue_fields']

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
            'issue_fields': self.DEFAULT_ISSUE_FIELDS
        }
        return config

    def _create_config(self, config_dict):
        self._create_config_dir()
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(yaml.dump(config_dict, default_flow_style=False))
        click.echo('Configuration file written to {}'.format(self.CONFIG_FILE))
