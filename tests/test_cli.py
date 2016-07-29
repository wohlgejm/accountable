from __future__ import absolute_import

from click.testing import CliRunner
import mock

from accountable import cli
from tests import support


@mock.patch('accountable.accountable.Accountable.projects')
def test_projects(mock_object):
    mock_object.return_value = support.projects()
    runner = CliRunner()
    result = runner.invoke(cli.projects)
    assert result.exit_code == 0
    assert result.output == '1 - AC - Accountable\n2 - EX - Example Project\n'


@mock.patch('accountable.accountable.Accountable.issue_types')
def test_issuetypes(mock_object):
    mock_object.return_value = support.issue_types()
    runner = CliRunner()
    result = runner.invoke(cli.issuetypes)
    assert result.exit_code == 0
    assert result.output == 'AC - 1 - Bug - An error in the code\n'


@mock.patch('accountable.accountable.Resource.get')
def test_issue(mock_object):
    mock_object.return_value = support.issue()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101'])
    assert result.exit_code == 0
    assert result.output == ('REPORTER - John Locke\nASSIGNEE - Jack Shepard\n'
                             'ISSUETYPE - Blocker\nSTATUS - In Progress\n'
                             'SUMMARY - Bug report\n'
                             'DESCRIPTION - example bug report\n')


@mock.patch('accountable.accountable.Resource.get')
def test_issue_comments(mock_object):
    mock_object.return_value = support.comments()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == ('10000 - fred - YUUUGE bug. - '
                             '2016-05-18T12:19:03.615+0000\n')


@mock.patch('accountable.accountable.Resource.get')
def test_issue_no_comments(mock_object):
    mock_object.return_value = {}
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == 'No comments found for DEV-101\n'


@mock.patch('accountable.accountable.Resource.post')
def test_addcomment(mock_object):
    mock_object.return_value = support.comments()['comments'][0]
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'addcomment', 'A comment'])
    assert result.exit_code == 0
    assert result.output == ('fred - YUUUGE bug. - '
                             '2016-05-18T12:19:03.615+0000\n')


@mock.patch('accountable.accountable.Resource.get')
def test_issue_worklog(mock_object):
    mock_object.return_value = support.issue_worklog()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'worklog'])
    assert result.exit_code == 0
    assert result.output == ('Author - fred\n'
                             'Comment - I did some work here.\n'
                             'Time spent - 3h 20m\n')


@mock.patch('accountable.accountable.Resource.get')
def test_issue_no_worklog(mock_object):
    mock_object.return_value = {}
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'worklog'])
    assert result.exit_code == 0
    assert result.output == 'No worklogs found for DEV-101\n'


@mock.patch('accountable.accountable.Resource.get')
def test_issue_transitions(mock_object):
    mock_object.return_value = support.issue_transitions()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'transitions'])
    assert result.exit_code == 0
    assert result.output == '2 - Close Issue\n711 - QA Review\n'


@mock.patch('accountable.accountable.Resource.get')
def test_issue_no_transitions(mock_object):
    mock_object.return_value = {}
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'transitions'])
    assert result.exit_code == 0
    assert result.output == 'No transitions found for DEV-101\n'


@mock.patch('accountable.accountable.Resource.post')
def test_do_transition(mock_object):
    mock_object.return_value = support.MockResponse(204)
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'dotransition', str(1)])
    assert result.exit_code == 0
    assert result.output == 'Successfully transitioned DEV-101\n'


@mock.patch('accountable.accountable.Resource.post')
def test_createissue_nargs(mock_object):
    mock_object.return_value = support.issue_create()
    runner = CliRunner()
    result = runner.invoke(cli.createissue, ['fields.project.id', '1'])
    assert result.exit_code == 0
    mock_object.assert_called_once_with('https://testdomain/rest/api/2/issue',
                                        {'fields': {'project': {'id': '1'}}})
    assert result.output == ('10000 - TST-24 - '
                             'http://www.example.com/jira/rest/api/2/issue/'
                             '10000\n')
