import os

import yaml
import click

from services.jira import Jira


class Accountable(object):
    CONFIG_DIR = os.path.expanduser('~/.accountable')
    CONFIG_FILE = '{}/config.yaml'.format(CONFIG_DIR)

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if kwargs.get('create_config'):
            self._initial_setup()
        self.config = self._load_config()
        self.username = self.config['username']
        self.password = self.config['password']
        self.domain = self.config['domain']
        self.client = Jira(self.username, self.password, self.domain)
        self.metadata = self.client.metadata()

    def _initial_setup(self):
        username = str(self.kwargs.get('username'))
        password = str(self.kwargs.get('password'))
        domain = str(self.kwargs.get('domain'))
        self._create_config(username, password, domain)

    def _create_config_dir(self):
        if not os.path.exists(self.CONFIG_DIR):
            click.echo('Creating {}'.format(self.CONFIG_DIR))
            os.makedirs(self.CONFIG_DIR)

    def _create_config(self, username, password, domain):
        self._create_config_dir()
        config = {'username': username, 'password': password, 'domain': domain}
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(yaml.dump(config, default_flow_style=False))
        click.echo('Configuration file written to {}'.format(self.CONFIG_FILE))

    def _load_config(self):
        with open(self.CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
        return config

    def projects(self):
        return [(project['key'],
                 project['name']) for project in self.metadata['projects']]

    def issue_types(self, project_key):
        if project_key:
            project = next(
                project for project in self.metadata['projects']
                if project['key'] == str(project_key)
            )
            return {project_key: project['issuetypes']}
        else:
            issue_types = {}
            for project in self.metadata['projects']:
                issue_types[project['key']] = project['issuetypes']
            return issue_types
