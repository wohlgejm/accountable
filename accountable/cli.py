from __future__ import absolute_import

import click

from accountable.accountable import Accountable


def prettyprint(*args):
    click.echo(' - '.join([arg for arg in args]))


@click.group()
def cli():
    """
    A Jira CLI.
    """
    pass


@click.command()
@click.option('--username', prompt='Your Jira username')
@click.option('--password', prompt='Your Jira password', hide_input=True)
@click.option('--domain', prompt='The domain where your account is hosted')
def configure(username, password, domain):
    """
    Initial configuration. Used to specify your username, password and domain.
    Configuration is stored in ~/.accountable/config.yaml.
    """
    Accountable(username=username,
                password=password,
                domain=domain,
                create_config=True)


@click.command()
def projects():
    """
    List all projects.
    """
    accountable = Accountable()
    projects = accountable.projects()
    for pid, key, name in projects:
        prettyprint(pid, key, name)


@click.command()
@click.argument('project_key', default='')
def issuetypes(project_key):
    """
    List all issue types. Optional parameter to list issue types by a given
    project.
    """
    accountable = Accountable()
    projects = accountable.issue_types(project_key)
    for key, issue_types in projects.items():
        for i in issue_types:
            prettyprint(key, i['id'], i['name'], i['description'])


@click.command()
@click.argument('options', nargs=-1)
def createissue(options):
    accountable = Accountable()
    issue = accountable.issue_create(options)
    prettyprint(issue['id'], issue['key'], issue['self'])


@click.group(invoke_without_command=True)
@click.argument('issue_key')
@click.pass_context
def issue(ctx, issue_key):
    """
    List metadata for a given issue key. Issue keys should take the format of
    {PROJECT-ID}-{ISSUE-ID}.
    """
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
    """
    Lists all comments for a given issue key.
    """
    accountable = Accountable()
    comments = accountable.issue_comments(ctx.obj['issue_key']).get('comments')
    if comments:
        for c in comments:
            prettyprint(c['id'], c['author']['name'], c['body'], c['created'])
    else:
        prettyprint('No comments found for {}'.format(ctx.obj['issue_key']))


@click.command()
@click.pass_context
@click.argument('body')
def addcomment(ctx, body):
    """
    Add a comment to the given issue key. Accepts a body argument to be used
    as the comment's body.
    """
    accountable = Accountable()
    r = accountable.issue_add_comment(ctx.obj['issue_key'], body)
    prettyprint(r['author']['name'], r['body'], r['created'])


@click.command()
@click.pass_context
def worklog(ctx):
    """
    List all worklogs for a given issue key.
    """
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
    """
    List all possible transitions for a given issue.
    """
    accountable = Accountable()
    transitions = accountable.issue_transitions(
        ctx.obj['issue_key']
    ).get('transitions')
    if transitions:
        for t in transitions:
            prettyprint(t['id'], t['name'])
    else:
        prettyprint('No transitions found for {}'.format(ctx.obj['issue_key']))


@click.command()
@click.pass_context
@click.argument('transition_id')
def dotransition(ctx, transition_id):
    """
    Transition the given issue to the provided ID. The API does not return a
    JSON response for this call.
    """
    accountable = Accountable()
    t = accountable.issue_do_transition(ctx.obj['issue_key'], transition_id)
    if t.status_code == 204:
        prettyprint(
            'Successfully transitioned {}'.format(ctx.obj['issue_key'])
        )


issue.add_command(dotransition)
issue.add_command(transitions)
issue.add_command(worklog)
issue.add_command(addcomment)
issue.add_command(comments)

cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
cli.add_command(issue)
cli.add_command(createissue)


if __name__ == '__main__':
    cli()
