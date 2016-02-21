from __future__ import absolute_import

from click.testing import CliRunner
import mock

from accountable import cli
from tests.support import projects, issue_types


@mock.patch('accountable.accountable.Accountable.projects')
def test_projects(mock_object):
    mock_object.return_value = projects()
    runner = CliRunner()
    result = runner.invoke(cli.projects)
    assert result.exit_code == 0
    assert result.output == 'AC - Accountable\nEX - Example Project\n'


@mock.patch('accountable.accountable.Accountable.issue_types')
def test_issuetypes(mock_object):
    mock_object.return_value = issue_types()
    runner = CliRunner()
    result = runner.invoke(cli.issuetypes)
    assert result.exit_code == 0
    assert result.output == 'AC - 1 - Bug - An error in the code\n'
