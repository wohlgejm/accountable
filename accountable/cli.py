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
@click.option('--domain', prompt='The base url of your Jira account')
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
            click.echo('{} - {} - {} - {}'.format(key,
                                                  i['id'],
                                                  i['name'],
                                                  i['description']))


@click.group()
@click.argument('issue_key')
@click.pass_context
def issue(ctx, issue_key):
    ctx.obj['ISSUE_KEY'] = issue_key


@click.command()
@click.pass_context
def worklog(ctx):
    click.echo(ctx.obj['ISSUE_KEY'])


cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
cli.add_command(issue)
issue.add_command(worklog)
