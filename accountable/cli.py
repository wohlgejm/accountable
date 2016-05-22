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


@click.group(invoke_without_command=True)
@click.argument('issue_key')
@click.pass_context
def issue(ctx, issue_key):
    ctx.obj = {}
    ctx.obj['issue_key'] = issue_key
    if not ctx.invoked_subcommand:
        accountable = Accountable()
        issue = accountable.issue_meta(issue_key)
        for field, value in issue.items():
            prettyprint(field, value)


@click.command()
@click.pass_context
def comments(ctx):
    accountable = Accountable()
    comments = accountable.issue_comments(ctx.obj['issue_key']).get('comments')
    if comments:
        for c in comments:
            prettyprint(c['author']['name'], c['body'],
                        c['created'])
    else:
        prettyprint('No comments found for {}'.format(ctx.obj['issue_key']))


@click.command()
@click.pass_context
@click.argument('body')
def addcomment(ctx, body):
    accountable = Accountable()
    r = accountable.issue_add_comment(ctx.obj['issue_key'], body)
    prettyprint(r['author']['name'], r['body'], r['created'])


@click.command()
@click.pass_context
def worklog(ctx):
    accountable = Accountable()
    worklog = accountable.issue_worklog(ctx.obj['issue_key']).get('worklogs')
    if worklog:
        for w in worklog:
            prettyprint('Author', w['author']['name'])
            prettyprint('Comment', w.get('comment'))
            prettyprint('Time spent', w['timeSpent'])
    else:
        prettyprint('No worklogs found for {}'.format(ctx.obj['issue_key']))


@click.command()
@click.pass_context
def transitions(ctx):
    accountable = Accountable()
    transitions = accountable.issue_worklog(ctx.obj['issue_key']).get('transitions')
    if transitions:
        for t in transitions:
            prettyprint(t['id'], t['name'])
    else:
        prettyprint('No transitions found for {}'.format(ctx.obj['issue_key']))


issue.add_command(transitions)
issue.add_command(worklog)
issue.add_command(addcomment)
issue.add_command(comments)

cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
cli.add_command(issue)
