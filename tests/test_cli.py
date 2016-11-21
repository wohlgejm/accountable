from __future__ import absolute_import

import os
import sys
import io

from click.testing import CliRunner
import mock
import requests
from doubles import no_builtin_verification, allow, expect
import pytest

from accountable import cli
from accountable.config import Config
from tests import support


@pytest.fixture
def fake_config():
    allow(Config).config_file.and_return(
        '{}/tests/config.yaml'.format(os.getcwd())
    )


def test_configure():
    with no_builtin_verification():
        i = __import__(('builtins' if sys.version_info >= (3,)
                        else '__builtin__'))
        allow(os.path).exists.and_return(False)
        expect(i).open.with_args(Config().config_file, 'w+').and_return(
            io.BytesIO()
        )
        expect(os).makedirs.with_args(Config.CONFIG_DIR)
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['configure'],
                               input='user\npassowrd\ndomain\n')
        assert result.exit_code == 0


@pytest.mark.usefixtures('fake_config')
class TestCommands(object):
    def test_projects(self):
        allow(requests).get.and_return(support.metadata_response())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['projects'])
        assert result.exit_code == 0
        assert result.output == '10000 - EX - Example Project\n' \
                                '10000 - AC - Accountable\n'

    def test_project_components(self):
        allow(requests).get.and_return(support.project_components())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['projectcomponents', 'SC'])
        assert result.exit_code == 0
        assert result.output == \
            '10000 - Component 1 - ' \
            'http://www.example.com/jira/rest/api/2/component/10000\n' \
            '10050 - PXA - ' \
            'http://www.example.com/jira/rest/api/2/component/10000\n'

    def test_issuetypes(self):
        allow(requests).get.and_return(support.metadata_response())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issuetypes'])
        assert result.exit_code == 0
        assert result.output == '1 - AC - Bug - An error in the code\n' \
                                '1 - EX - Bug - An error in the code\n'

    def test_issuetypes_project(self):
        allow(requests).get.and_return(support.metadata_response())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issuetypes', 'AC'])
        assert result.exit_code == 0
        assert result.output == '1 - AC - Bug - An error in the code\n'

    def test_issue(self):
        allow(requests).get.and_return(support.issue())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101'])
        assert result.exit_code == 0
        assert result.output == (
            'REPORTER - John Locke\nASSIGNEE - Jack Shepard\n'
            'ISSUETYPE - Blocker\nSTATUS - In Progress\n'
            'SUMMARY - Bug report\n'
            'DESCRIPTION - example bug report\n'
        )

    def test_issue_comments(self):
        allow(requests).get.and_return(support.comments())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'comments'])
        assert result.exit_code == 0
        assert result.output == ('10000 - fred - YUUUGE bug. - '
                                 '2016-05-18T12:19:03.615+0000\n')

    def test_issue_no_comments(self):
        response = support.MockResponse(200)
        response.data = {}
        allow(requests).get.and_return(response)
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'comments'])
        assert result.exit_code == 0
        assert result.output == 'No comments found for DEV-101\n'

    def test_addcomment(self):
        allow(requests).post.and_return(support.comment())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'addcomment',
                                         'A comment'])
        assert result.exit_code == 0
        assert result.output == ('fred - YUUUGE bug. - '
                                 '2016-05-18T12:19:03.615+0000\n')

    def test_issue_worklog(self):
        allow(Config).config_file.and_return(
            '{}/tests/config.yaml'.format(os.getcwd())
        )
        allow(requests).get.and_return(support.issue_worklog())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'worklog'])
        assert result.exit_code == 0
        assert result.output == ('Author - fred\n'
                                 'Comment - I did some work here.\n'
                                 'Time spent - 3h 20m\n')

    def test_issue_no_workloga(self):
        response = support.MockResponse(200)
        response.data = {}
        allow(requests).get.and_return(response)
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'worklog'])
        assert result.exit_code == 0
        assert result.output == 'No worklogs found for DEV-101\n'

    def test_issue_transitions(self):
        allow(requests).get.and_return(support.issue_transitions())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'transitions'])
        assert result.exit_code == 0
        assert result.output == '2 - Close Issue\n711 - QA Review\n'

    def test_issue_no_transitions(self):
        allow(Config).config_file.and_return(
            '{}/tests/config.yaml'.format(os.getcwd())
        )
        response = support.MockResponse(200)
        response.data = {}
        allow(requests).get.and_return(response)
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'transitions'])
        assert result.exit_code == 0
        assert result.output == 'No transitions found for DEV-101\n'

    def test_do_transition(self):
        transition = support.MockResponse(204)
        transition.data = float('-inf')
        allow(requests).post.and_return(transition)
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101',
                                         'dotransition', str(1)])
        assert result.exit_code == 0
        assert result.output == 'Successfully transitioned DEV-101\n'

    def test_createissue_nargs(self):
        allow(requests).post.and_return(support.issue_create())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['createissue', 'project.id', '1'])
        assert result.exit_code == 0
        assert result.output == (
            '10000 - TST-24 - '
            'http://www.example.com/jira/rest/api/2/issue/10000\n'
        )

    @mock.patch('accountable.accountable.Accountable._repo')
    def test_checkoutbranch(self, mock_repo):
        allow(Config).config_file.and_return(
            '{}/tests/config.yaml'.format(os.getcwd())
        )
        allow(requests).post.and_return(support.issue_create())
        mock_repo.return_value = support.MockRepo()
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['checkoutbranch', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == (
            '10000 - TST-24 - '
            'http://www.example.com/jira/rest/api/2/issue/10000\n'
        )

    @mock.patch('accountable.accountable.Accountable._repo')
    def test_checkout(self, mock_repo):
        allow(requests).get.and_return(support.issue())
        mock_repo.return_value = support.MockRepo()
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['checkout', 'TST-24'])
        assert result.exit_code == 0
        assert result.output == (
            '10002 - EX-1 - '
            'http://www.example.com/jira/rest/api/2/issue/10002\n'
        )

    @mock.patch('accountable.accountable.Accountable._repo')
    def test_cob(self, mock_repo):
        allow(requests).post.and_return(support.issue_create())
        mock_repo.return_value = support.MockRepo()
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['cob', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == (
            '10000 - TST-24 - '
            'http://www.example.com/jira/rest/api/2/issue/10000\n'
        )

    @mock.patch('accountable.accountable.Accountable._repo')
    def test_custom_alias(self, mock_repo):
        allow(requests).post.and_return(support.issue_create())
        mock_repo.return_value = support.MockRepo()
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['custom', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == (
            '10000 - TST-24 - '
            'http://www.example.com/jira/rest/api/2/issue/10000\n'
        )

    @mock.patch('accountable.accountable.Accountable._repo')
    def test_alias_not_found(self, mock_repo):
        allow(requests).post.and_return(support.issue_create())
        mock_repo.return_value = support.MockRepo()
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['notthere', 'project.id',
                                         '1', 'summary', 'slug me'])
        assert result.exit_code == 2
        assert result.output == 'Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n' \
                                'Error: No such command "notthere".\n'

    def test_users(self):
        allow(requests).get.and_return(support.users())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['users', 'e'])
        assert result.exit_code == 0
        assert result.output == ('fred - Fred F. User\n'
                                 'andrew - Andrew Anderson\n')
