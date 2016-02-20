import click

from accountable import Accountable


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
        click.echo('{} - {}'.format(key, name))


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


cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
