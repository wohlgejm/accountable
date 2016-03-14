from __future__ import absolute_import

import click

from accountable.accountable import Accountable


def prettyprint(*args):
    click.echo(' - '.join([arg for arg in args]))


@click.group()
def cli():
    pass


@click.command()
@click.option('--username', prompt='Your Jira username')
@click.option('--password', prompt='Your Jira password', hide_input=True)
@click.option('--domain', prompt='The domain where your account is hosted')
def configure(username, password, domain):
    Accountable(username=username,
                password=password,
                domain=domain,
                create_config=True)


@click.command()
def projects():
    accountable = Accountable()
    projects = accountable.projects()
    for key, name in projects:
        prettyprint(key, name)


@click.command()
@click.argument('project_key', default='')
def issuetypes(project_key):
    accountable = Accountable()
    projects = accountable.issue_types(project_key)
    for key, issue_types in projects.items():
        for i in issue_types:
            prettyprint(key, i['id'], i['name'], i['description'])


@click.command()
@click.argument('issue_key')
def issue(issue_key):
    accountable = Accountable()
    issue = accountable.issue_meta(issue_key)
    for field, value in issue.items():
        prettyprint(field, value)


cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
cli.add_command(issue)
