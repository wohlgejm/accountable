from __future__ import absolute_import

from click.testing import CliRunner
import mock

from accountable import cli
from tests import support


@mock.patch('accountable.accountable.Accountable.projects')
def test_projects(mock_object):
    mock_object.return_value = support.projects()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['projects'])
    assert result.exit_code == 0
    assert result.output == '1 - AC - Accountable\n2 - EX - Example Project\n'


@mock.patch('accountable.accountable.Accountable.issue_types')
def test_issuetypes(mock_object):
    mock_object.return_value = support.issue_types().json()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issuetypes'])
    assert result.exit_code == 0
    assert result.output == '1 - AC - Bug - An error in the code\n'


@mock.patch('requests.get')
def test_issue(mock_object):
    mock_object.return_value = support.issue()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101'])
    assert result.exit_code == 0
    assert result.output == ('REPORTER - John Locke\nASSIGNEE - Jack Shepard\n'
                             'ISSUETYPE - Blocker\nSTATUS - In Progress\n'
                             'SUMMARY - Bug report\n'
                             'DESCRIPTION - example bug report\n')


@mock.patch('requests.get')
def test_issue_comments(mock_object):
    mock_object.return_value = support.comments()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == ('10000 - fred - YUUUGE bug. - '
                             '2016-05-18T12:19:03.615+0000\n')


@mock.patch('requests.get')
def test_issue_no_comments(mock_object):
    response = support.MockResponse(200)
    response.data = {}
    mock_object.return_value = response
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == 'No comments found for DEV-101\n'


@mock.patch('requests.post')
def test_addcomment(mock_object):
    mock_object.return_value = support.comment()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'addcomment',
                                     'A comment'])
    assert result.exit_code == 0
    assert result.output == ('fred - YUUUGE bug. - '
                             '2016-05-18T12:19:03.615+0000\n')


@mock.patch('requests.get')
def test_issue_worklog(mock_object):
    mock_object.return_value = support.issue_worklog()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'worklog'])
    assert result.exit_code == 0
    assert result.output == ('Author - fred\n'
                             'Comment - I did some work here.\n'
                             'Time spent - 3h 20m\n')


@mock.patch('requests.get')
def test_issue_no_worklog(mock_object):
    response = support.MockResponse(200)
    response.data = {}
    mock_object.return_value = response
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'worklog'])
    assert result.exit_code == 0
    assert result.output == 'No worklogs found for DEV-101\n'


@mock.patch('requests.get')
def test_issue_transitions(mock_object):
    mock_object.return_value = support.issue_transitions()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'transitions'])
    assert result.exit_code == 0
    assert result.output == '2 - Close Issue\n711 - QA Review\n'


@mock.patch('requests.get')
def test_issue_no_transitions(mock_object):
    response = support.MockResponse(200)
    response.data = {}
    mock_object.return_value = response
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'transitions'])
    assert result.exit_code == 0
    assert result.output == 'No transitions found for DEV-101\n'


@mock.patch('requests.post')
def test_do_transition(mock_post):
    transition = support.MockResponse(204)
    transition.data = float('-inf')
    mock_post.return_value = transition
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['issue', 'DEV-101',
                                     'dotransition', str(1)])
    assert result.exit_code == 0
    assert result.output == 'Successfully transitioned DEV-101\n'


@mock.patch('requests.post')
def test_createissue_nargs(mock_post):
    mock_post.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['createissue', 'project.id', '1'])
    assert result.exit_code == 0
    assert result.output == ('10000 - TST-24 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10000\n')


@mock.patch('accountable.accountable.Accountable._repo')
@mock.patch('requests.post')
def test_checkoutbranch(mock_post, mock_repo):
    mock_repo.return_value = support.MockRepo()
    mock_post.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.cli,
                           ['checkoutbranch', 'project.id', '1',
                            'summary', 'slug me'])
    assert result.exit_code == 0
    assert result.output == ('10000 - TST-24 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10000\n')


@mock.patch('accountable.accountable.Accountable._repo')
@mock.patch('requests.get')
def test_checkout(mock_get, mock_repo):
    mock_repo.return_value = support.MockRepo()
    mock_get.return_value = support.issue()
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['checkout', 'TST-24'])
    assert result.exit_code == 0
    assert result.output == ('10002 - EX-1 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10002\n')


@mock.patch('accountable.accountable.Accountable._repo')
@mock.patch('requests.post')
def test_cob(mock_post, mock_repo):
    mock_repo.return_value = support.MockRepo()
    mock_post.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.cli,
                           ['cob', 'project.id', '1', 'summary', 'slug me'])
    assert result.exit_code == 0
    assert result.output == ('10000 - TST-24 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10000\n')


@mock.patch('accountable.accountable.Accountable._repo')
@mock.patch('requests.post')
@mock.patch('accountable.accountable.Accountable.aliases')
def test_custom_alias(mock_aliases, mock_post, mock_repo):
    mock_aliases.return_value = {'custom': 'checkoutbranch'}
    mock_repo.return_value = support.MockRepo()
    mock_post.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.cli,
                           ['custom', 'project.id', '1', 'summary', 'slug me'])
    assert result.exit_code == 0
    assert result.output == ('10000 - TST-24 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10000\n')


@mock.patch('accountable.accountable.Accountable._repo')
@mock.patch('requests.post')
def test_alias_not_found(mock_post, mock_repo):
    mock_repo.return_value = support.MockRepo()
    mock_post.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.cli,
                           ['notthere', 'project.id', '1', 'summary',
                            'slug me'])
    assert result.exit_code == 2
    assert result.output == 'Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n' \
                            'Error: No such command "notthere".\n'


@mock.patch('requests.get')
def test_users(mock_get):
    mock_get.return_value = support.users()
    runner = CliRunner()
    result = runner.invoke(cli.cli,
                           ['users', 'e'])
    assert result.exit_code == 0
    assert result.output == ('fred - Fred F. User\n'
                             'andrew - Andrew Anderson\n')
