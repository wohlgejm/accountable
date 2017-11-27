from __future__ import absolute_import

from functools import update_wrapper
from operator import itemgetter
import textwrap

import click
from terminaltables import SingleTable

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


def print_table(table):
    for row_idx, row in enumerate(table.table_data):
        for col_idx, _col in enumerate(row):
            max_width = table.column_max_width(col_idx)
            datum = table.table_data[row_idx][col_idx]
            if max_width > 0 and len(str(datum)) >= max_width:
                table.table_data[row_idx][col_idx] = '\n'.join(
                    textwrap.wrap(datum, max_width)
                )
    click.echo(table.table)


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
    art = r'''
Welcome!                                __        ___.   .__
_____    ____  ____  ____  __ __  _____/  |______ \_ |__ |  |   ____
\__  \ _/ ___\/ ___\/  _ \|  |  \/    \   __\__  \ | __ \|  | _/ __ \
 / __ \\  \__\  \__(  <_> )  |  /   |  \  |  / __ \| \_\ \  |_\  ___/
(____  /\___  >___  >____/|____/|___|  /__| (____  /___  /____/\___  >
     \/     \/    \/                 \/          \/    \/          \/
     '''
    click.secho(art, fg='blue')
    Config(username=username, password=password, domain=domain)


@click.command()
@pass_accountable
def projects(accountable):
    """
    List all projects.
    """
    projects = accountable.metadata()['projects']
    headers = sorted(['id', 'key', 'self'])
    rows = [[v for k, v in sorted(p.items()) if k in headers] for p in projects]
    rows.insert(0, headers)
    print_table(SingleTable(rows))


@click.command()
@click.argument('project_key', default='')
@pass_accountable
def issuetypes(accountable, project_key):
    """
    List all issue types. Optional parameter to list issue types by a given
    project.
    """
    projects = accountable.issue_types(project_key)
    headers = sorted(['id', 'name', 'description'])
    rows = []
    for key, issue_types in sorted(projects.items()):
        for issue_type in issue_types:
            rows.append(
                [key] + [v for k, v in sorted(issue_type.items())
                         if k in headers]
            )
    rows.insert(0, ['project_key'] + headers)
    print_table(SingleTable(rows))


@click.command()
@click.argument('project_key', required=True)
@pass_accountable
def components(accountable, project_key):
    """
    Returns a list of all a project's components.
    """
    components = accountable.project_components(project_key)
    headers = sorted(['id', 'name', 'self'])
    rows = [[v for k, v in sorted(component.items()) if k in headers]
            for component in components]
    rows.insert(0, headers)
    print_table(SingleTable(rows))


def nargs(f):
    @click.argument('options', nargs=-1)
    @pass_accountable
    @click.pass_context
    def new_func(ctx, accountable, options, *args, **kwargs):
        return ctx.invoke(f, accountable, options, *args, **kwargs)
    return update_wrapper(new_func, f)


@click.command()
@click.argument('project_key', required=True)
@click.argument('issue_type', required=False)
@pass_accountable
def createmeta(accountable, project_key, issue_type=None):
    """
    Create new issue.
    """
    metadata = accountable.create_meta(project_key, issue_type)
    headers = [
        'project_key', 'issuetype_name', 'field_key', 'field_name', 'required'
    ]
    rows = [headers]
    for project in metadata:
        key = project['key']
        issuetypes = project['issuetypes']
        for issuetype in issuetypes:
            name = issuetype['name']
            fields = issuetype['fields']
            for k, v in fields.items():
                field_key = k
                field_name = v['name']
                required = v['required']
                rows.append([key, name, field_key, field_name, required])
    print_table(SingleTable(rows))


@click.command()
@nargs
def createissue(accountable, options):
    """
    Create new issue.
    """
    issue = accountable.issue_create(options)
    headers = sorted(['id', 'key', 'self'])
    rows = [headers, [itemgetter(header)(issue) for header in headers]]
    print_table(SingleTable(rows))


@click.command()
@nargs
def checkoutbranch(accountable, options):
    """
    Create a new issue and checkout a branch named after it.
    """
    issue = accountable.checkout_branch(options)
    headers = sorted(['id', 'key', 'self'])
    rows = [headers, [itemgetter(header)(issue) for header in headers]]
    print_table(SingleTable(rows))


@click.command()
@click.argument('issue_key')
@pass_accountable
def checkout(accountable, issue_key):
    """
    Checkout a new branch or checkout to a branch for a given issue.
    """
    issue = accountable.checkout(issue_key)
    headers = issue.keys()
    rows = [headers, [v for k, v in issue.items()]]
    print_table(SingleTable(rows))


@click.group(invoke_without_command=True)
@click.argument('issue_key')
@pass_accountable
@click.pass_context
def issue(ctx, accountable, issue_key):
    """
    List metadata for a given issue key.
    """
    accountable.issue_key = issue_key
    if not ctx.invoked_subcommand:
        issue = accountable.issue_meta()
        headers = issue.keys()
        rows = [headers, [v for k, v in issue.items()]]
        print_table(SingleTable(rows))


@click.command()
@nargs
def update(accountable, options):
    """
    Update an existing issue.
    """
    issue = accountable.issue_update(options)
    headers = issue.keys()
    rows = [headers, [v for k, v in issue.items()]]
    print_table(SingleTable(rows))


@click.command()
@pass_accountable
def comments(accountable):
    """
    Lists all comments for a given issue key.
    """
    comments = accountable.issue_comments()
    headers = sorted(['author_name', 'body', 'updated'])

    if comments:
        rows = [[v for k, v in sorted(c.items()) if k in headers]
                for c in comments]
        rows.insert(0, headers)
        print_table(SingleTable(rows))
    else:
        click.secho('No comments found for {}'.format(
            accountable.issue_key
        ), fg='red')


@click.command()
@click.argument('body')
@pass_accountable
def addcomment(accountable, body):
    """
    Add a comment to the given issue key. Accepts a body argument to be used
    as the comment's body.
    """

    r = accountable.issue_add_comment(body)
    headers = sorted(['author_name', 'body', 'updated'])
    rows = [[v for k, v in sorted(r.items()) if k in headers]]
    rows.insert(0, headers)
    print_table(SingleTable(rows))


@click.command()
@pass_accountable
def worklog(accountable):
    """
    List all worklogs for a given issue key.
    """
    worklog = accountable.issue_worklog()
    headers = ['author_name', 'comment', 'time_spent']
    if worklog:
        rows = [[v for k, v in sorted(w.items()) if k in headers]
                for w in worklog]
        rows.insert(0, headers)
        print_table(SingleTable(rows))
    else:
        click.secho(
            'No worklogs found for {}'.format(accountable.issue_key),
            fg='red'
        )


@click.command()
@pass_accountable
def transitions(accountable):
    """
    List all possible transitions for a given issue.
    """
    transitions = accountable.issue_transitions().get('transitions')
    headers = ['id', 'name']
    if transitions:
        rows = [[v for k, v in sorted(t.items()) if k in headers]
                for t in transitions]
        rows.insert(0, headers)
        print_table(SingleTable(rows))
    else:
        click.secho(
            'No transitions found for {}'.format(accountable.issue_key),
            fg='red'
        )


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
        click.secho(
            'Successfully transitioned {}'.format(accountable.issue_key),
            fg='green'
        )


@click.command()
@pass_accountable
@click.argument('query')
def users(accountable, query):
    """
    Executes a user search for the given query.
    """
    users = accountable.users(query)
    headers = ['display_name', 'key']
    if users:
        rows = [[v for k, v in sorted(u.items()) if k in headers]
                for u in users]
        rows.insert(0, headers)
        print_table(SingleTable(rows))
    else:
        click.secho('No users found for query {}'.format(
            query
        ), fg='red')


issue.add_command(dotransition)
issue.add_command(transitions)
issue.add_command(worklog)
issue.add_command(addcomment)
issue.add_command(comments)
issue.add_command(update)

cli.add_command(configure)
cli.add_command(projects)
cli.add_command(issuetypes)
cli.add_command(issue)
cli.add_command(createissue)
cli.add_command(users)
cli.add_command(checkoutbranch)
cli.add_command(checkout)
cli.add_command(components)
cli.add_command(createmeta)


if __name__ == '__main__':
    cli()
