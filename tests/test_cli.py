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
    assert result.output == 'AC - Accountable\nEX - Example Project\n'


@mock.patch('accountable.accountable.Accountable.issue_types')
def test_issuetypes(mock_object):
    mock_object.return_value = support.issue_types()
    runner = CliRunner()
    result = runner.invoke(cli.issuetypes)
    assert result.exit_code == 0
    assert result.output == 'AC - 1 - Bug - An error in the code\n'


@mock.patch('accountable.jira.Jira.issue')
def test_issue(mock_object):
    mock_object.return_value = support.issue()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101'])
    assert result.exit_code == 0
    assert result.output == ('REPORTER - John Locke\nASSIGNEE - Jack Shepard\n'
                             'ISSUETYPE - Blocker\nSTATUS - In Progress\n'
                             'SUMMARY - Bug report\n'
                             'DESCRIPTION - example bug report\n')


@mock.patch('accountable.jira.Jira.issue_comments')
def test_issue_comments(mock_object):
    mock_object.return_value = support.comments()
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == ('fred - YUUUGE bug. - '
                             '2016-05-18T12:19:03.615+0000\n')


@mock.patch('accountable.jira.Jira.issue_comments')
def test_issue_no_comments(mock_object):
    mock_object.return_value = {}
    runner = CliRunner()
    result = runner.invoke(cli.issue, ['DEV-101', 'comments'])
    assert result.exit_code == 0
    assert result.output == ('No comments found for DEV-101\n')
