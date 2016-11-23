import os


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


class Config(object):

    def __init__(self):
        self._config = None

    def __getitem__(self, name):
        return self.config[name]

    def __repr__(self):
        '{}({})'.format(self.__class__, self.config)

    def create(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        domain = kwargs.get('domain')
        config_dict = self._config_dict(username, password, domain)
        self._create_config(config_dict)

    @property
    def auth(self):
        return HTTPBasicAuth(self['username'], self['password'])

    @property
    def config(self):
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
        return config

    def _create_config_dir(self):
        if not os.path.exists(CONFIG_DIR):
            click.echo('Creating {}'.format(CONFIG_DIR))
            os.makedirs(CONFIG_DIR)

    def _config_dict(self, username, password, domain):
        return {
            'username': username,
            'password': password,
            'domain': domain,
            'issue_fields': DEFAULT_ISSUE_FIELDS,
            'aliases': DEFAULT_ALIASES
        }

    def _create_config(self, config_dict):
        self._create_config_dir()
        with open(CONFIG_FILE, 'w+') as f:
            f.write(yaml.dump(config_dict, default_flow_style=False,
                              encoding='utf-8'))
        click.echo('Configuration file written to {}'.format(CONFIG_FILE))
