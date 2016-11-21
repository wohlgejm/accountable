from __future__ import absolute_import

from functools import update_wrapper

import click

from accountable.accountable import Accountable, Config


pass_accountable = click.make_pass_decorator(Accountable)


class AccountableCli(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        alias = Config()['aliases'].get(cmd_name, None)
        if alias is not None:
            return click.Group.get_command(self, ctx, alias)
        return None


def prettyprint(output):
    if isinstance(output, list):
        for i in output:
            click.echo(' - '.join([x for x in i]))
    else:
        click.echo(' - '.join([x for x in output]))


@click.group(cls=AccountableCli)
@click.pass_context
def cli(ctx):
    """
    A Jira CLI.
    """
    ctx.obj = Accountable()


@click.command()
@click.option('--username', prompt='Your Jira username')
@click.option('--password', prompt='Your Jira password', hide_input=True)
@click.option('--domain', prompt='The domain where your account is hosted')
def configure(username, password, domain):
    """
    Initial configuration. Used to specify your username, password and domain.
    Configuration is stored in ~/.accountable/config.yaml.
    """
    Config().create(username=username, password=password, domain=domain)


@click.command()
@pass_accountable
def projects(accountable):
    """
    List all projects.
    """
    projects = accountable.projects()
    for pid, key, name in projects:
        prettyprint((pid, key, name))


@click.command()
@click.argument('project_key', default='')
@pass_accountable
def issuetypes(accountable, project_key):
    """
    List all issue types. Optional parameter to list issue types by a given
    project.
    """
    projects = accountable.issue_types(project_key)
    for key, issue_types in sorted(projects.items()):
        for i in issue_types:
            prettyprint((i['id'], key, i['name'], i['description']))


def nargs(f):
    @click.argument('options', nargs=-1)
    @pass_accountable
    @click.pass_context
    def new_func(ctx, accountable, options, *args, **kwargs):
        return ctx.invoke(f, accountable, options, *args, **kwargs)
    return update_wrapper(new_func, f)


@click.command()
@nargs
def createissue(accountable, options):
    """
    Create new issue.
    """
    issue = accountable.issue_create(options)
    prettyprint((issue['id'], issue['key'], issue['self']))


@click.command()
@nargs
def checkoutbranch(accountable, options):
    """
    Create a new issue and checkout a branch named after it.
    """
    issue = accountable.checkout_branch(options)
    prettyprint((issue['id'], issue['key'], issue['self']))


@click.command()
@click.argument('issue_key')
@pass_accountable
def checkout(accountable, issue_key):
    """
    Checkout a new branch or checkout to a branch for a given issue.
    """
    issue = accountable.checkout(issue_key)
    prettyprint((issue['id'], issue['key'], issue['self']))


@click.group(invoke_without_command=True)
@click.argument('issue_key')
@pass_accountable
@click.pass_context
def issue(ctx, accountable, issue_key):
    """
    List metadata for a given issue key. Issue keys should take the format of
    {PROJECT-ID}-{ISSUE-ID}.
    """
    accountable.issue_key = issue_key
    if not ctx.invoked_subcommand:
        issue = accountable.issue_meta()
        for field, value in issue.items():
            prettyprint((field, value))


@click.command()
@pass_accountable
def comments(accountable):
    """
    Lists all comments for a given issue key.
    """
    comments = accountable.issue_comments().get('comments')
    if comments:
        for c in comments:
            prettyprint((c['id'], c['author']['name'], c['body'],
                         c['created']))
    else:
        prettyprint(('No comments found for {}'.format(
            accountable.issue_key), )
        )


@click.command()
@click.argument('body')
@pass_accountable
def addcomment(accountable, body):
    """
    Add a comment to the given issue key. Accepts a body argument to be used
    as the comment's body.
    """
    r = accountable.issue_add_comment(body)
    prettyprint((r['author']['name'], r['body'], r['created']))


@click.command()
@pass_accountable
def worklog(accountable):
    """
    List all worklogs for a given issue key.
    """
    worklog = accountable.issue_worklog().get('worklogs')
    if worklog:
        for w in worklog:
            prettyprint(('Author', w['author']['name']))
            prettyprint(('Comment', w.get('comment')))
            prettyprint(('Time spent', w['timeSpent']))
    else:
        prettyprint(('No worklogs found for {}'.format(accountable.issue_key),
                     ))


@click.command()
@pass_accountable
def transitions(accountable):
    """
    List all possible transitions for a given issue.
    """
    transitions = accountable.issue_transitions().get('transitions')
    if transitions:
        for t in transitions:
            prettyprint((t['id'], t['name']))
    else:
        prettyprint(('No transitions found for {}'.format(
            accountable.issue_key),
        ))


@click.command()
@pass_accountable
@click.argument('transition_id')
def dotransition(accountable, transition_id):
    """
    Transition the given issue to the provided ID. The API does not return a
    JSON response for this call.
    """
    t = accountable.issue_do_transition(transition_id)
    if t.status_code == 204:
        prettyprint((
            'Successfully transitioned {}'.format(accountable.issue_key),
        ))


@click.command()
@pass_accountable
@click.argument('query')
def users(accountable, query):
    """
    Executes a user search for the given query.
    """
    users = accountable.users(query)
    prettyprint([(user['key'], user['displayName']) for user in users])


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
cli.add_command(users)
cli.add_command(checkoutbranch)
cli.add_command(checkout)


if __name__ == '__main__':
    cli()
