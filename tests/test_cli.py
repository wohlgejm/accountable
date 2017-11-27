# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import io

from click.testing import CliRunner
import requests
from doubles import (no_builtin_verification, allow, expect, ClassDouble,
                     allow_constructor, InstanceDouble)
import pytest

from accountable import cli
from accountable import config
from accountable import accountable
from tests import support


@pytest.fixture
def git():
    repo = ClassDouble('accountable.accountable.Repo')
    git = InstanceDouble('accountable.accountable.Repo')
    git.git = support.MockRepo()
    allow_constructor(repo).and_return(git)
    accountable.Repo = repo


@pytest.fixture
def fake_config():
    config.CONFIG_FILE = '{}/tests/config.yaml'.format(os.getcwd())


def test_configure():
    with no_builtin_verification():
        i = __import__(('builtins' if sys.version_info >= (3,)
                        else '__builtin__'))
        allow(os.path).exists.and_return(False)
        allow(os.path).isfile.and_return(False)
        expect(i).open.with_args(config.CONFIG_FILE, 'w+').and_return(
            io.BytesIO()
        )
        expect(os).makedirs.with_args(config.CONFIG_DIR)
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
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B key \x1b(0x\x1b(B self                                              \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B EX  \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/project/EX \x1b(0x\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B AC  \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/project/AC \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_components(self):
        allow(requests).get.and_return(support.project_components())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['components', 'SC'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B name       \x1b(0x\x1b(B self                                                   \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10001 \x1b(0x\x1b(B Component1 \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/component/10000 \x1b(0x\x1b(B\n\x1b(0x\x1b(B 10050 \x1b(0x\x1b(B PXA        \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/component/10000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_issuetypes(self):
        allow(requests).get.and_return(support.metadata_response())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issuetypes'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqwqqqqwqqqqqqk\x1b(B\n\x1b(0x\x1b(B project_key \x1b(0x\x1b(B description          \x1b(0x\x1b(B id \x1b(0x\x1b(B name \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqnqqqqnqqqqqqu\x1b(B\n\x1b(0x\x1b(B AC          \x1b(0x\x1b(B An error in the code \x1b(0x\x1b(B 1  \x1b(0x\x1b(B Bug  \x1b(0x\x1b(B\n\x1b(0x\x1b(B EX          \x1b(0x\x1b(B An error in the code \x1b(0x\x1b(B 1  \x1b(0x\x1b(B Bug  \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqvqqqqvqqqqqqj\x1b(B\n'

    def test_issuetypes_project(self):
        allow(requests).get.and_return(support.metadata_response())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issuetypes', 'AC'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqwqqqqwqqqqqqk\x1b(B\n\x1b(0x\x1b(B project_key \x1b(0x\x1b(B description          \x1b(0x\x1b(B id \x1b(0x\x1b(B name \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqnqqqqnqqqqqqu\x1b(B\n\x1b(0x\x1b(B AC          \x1b(0x\x1b(B An error in the code \x1b(0x\x1b(B 1  \x1b(0x\x1b(B Bug  \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqvqqqqvqqqqqqj\x1b(B\n'

    def test_issue(self, get_issue):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B assignee_display_name \x1b(0x\x1b(B description        \x1b(0x\x1b(B reporter_display_name \x1b(0x\x1b(B status_status_category_name \x1b(0x\x1b(B summary    \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B Jack Shepard          \x1b(0x\x1b(B example bug report \x1b(0x\x1b(B John Locke            \x1b(0x\x1b(B In Progress                 \x1b(0x\x1b(B Bug report \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj\x1b(B\n'

    def test_issue_update(self, get_issue):
        allow(config.Config).auth
        expect(requests).put.and_return(support.MockResponse(204))
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'update',
                                         'reporter.name', 'james'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B assignee_display_name \x1b(0x\x1b(B description        \x1b(0x\x1b(B reporter_display_name \x1b(0x\x1b(B status_status_category_name \x1b(0x\x1b(B summary    \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B Jack Shepard          \x1b(0x\x1b(B example bug report \x1b(0x\x1b(B John Locke            \x1b(0x\x1b(B In Progress                 \x1b(0x\x1b(B Bug report \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj\x1b(B\n'

    def test_issue_comments(self):
        allow(requests).get.and_return(support.comments())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'comments'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqwqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B author_name \x1b(0x\x1b(B body        \x1b(0x\x1b(B updated                      \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqnqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B fred        \x1b(0x\x1b(B YUUUGE bug. \x1b(0x\x1b(B 2016-05-18T12:19:03.615+0000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

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
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqwqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B author_name \x1b(0x\x1b(B body        \x1b(0x\x1b(B updated                      \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqnqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B fred        \x1b(0x\x1b(B YUUUGE bug. \x1b(0x\x1b(B 2016-05-18T12:19:03.615+0000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_issue_worklog(self):
        allow(requests).get.and_return(support.issue_worklog())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['issue', 'DEV-101', 'worklog'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B author_name \x1b(0x\x1b(B comment               \x1b(0x\x1b(B time_spent \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B fred        \x1b(0x\x1b(B I did some work here. \x1b(0x\x1b(B 3h 20m     \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj\x1b(B\n'

    def test_issue_no_worklog(self):
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
        assert result.output == u'\x1b(0lqqqqqwqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id  \x1b(0x\x1b(B name        \x1b(0x\x1b(B\n\x1b(0tqqqqqnqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 2   \x1b(0x\x1b(B Close Issue \x1b(0x\x1b(B\n\x1b(0x\x1b(B 711 \x1b(0x\x1b(B QA Review   \x1b(0x\x1b(B\n\x1b(0mqqqqqvqqqqqqqqqqqqqj\x1b(B\n'

    def test_issue_no_transitions(self):
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
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B key    \x1b(0x\x1b(B self                                               \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B TST-24 \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/issue/10000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_checkoutbranch(self, git):
        allow(requests).post.and_return(support.issue_create())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['checkoutbranch', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B key    \x1b(0x\x1b(B self                                               \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B TST-24 \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/issue/10000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_checkout(self, git):
        allow(requests).get.and_return(support.issue())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['checkout', 'TST-24'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqwqqqqqqqwqqqqqqk\x1b(B\n\x1b(0x\x1b(B self                                               \x1b(0x\x1b(B id    \x1b(0x\x1b(B key  \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqnqqqqqqu\x1b(B\n\x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/issue/10002 \x1b(0x\x1b(B 10002 \x1b(0x\x1b(B EX-1 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqvqqqqqqj\x1b(B\n'

    def test_cob(self, git):
        allow(requests).post.and_return(support.issue_create())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['cob', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B key    \x1b(0x\x1b(B self                                               \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B TST-24 \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/issue/10000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_custom_alias(self, git):
        allow(requests).post.and_return(support.issue_create())
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['custom', 'project.id', '1',
                                         'summary', 'slug me'])
        assert result.exit_code == 0
        assert result.output == u'\x1b(0lqqqqqqqwqqqqqqqqwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B id    \x1b(0x\x1b(B key    \x1b(0x\x1b(B self                                               \x1b(0x\x1b(B\n\x1b(0tqqqqqqqnqqqqqqqqnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B 10000 \x1b(0x\x1b(B TST-24 \x1b(0x\x1b(B http://www.example.com/jira/rest/api/2/issue/10000 \x1b(0x\x1b(B\n\x1b(0mqqqqqqqvqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj\x1b(B\n'

    def test_alias_not_found(self, git):
        allow(requests).post.and_return(support.issue_create())
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
        assert result.output == u'\x1b(0lqqqqqqqqqqqqqqqqqwqqqqqqqqk\x1b(B\n\x1b(0x\x1b(B display_name    \x1b(0x\x1b(B key    \x1b(0x\x1b(B\n\x1b(0tqqqqqqqqqqqqqqqqqnqqqqqqqqu\x1b(B\n\x1b(0x\x1b(B Fred F. User    \x1b(0x\x1b(B fred   \x1b(0x\x1b(B\n\x1b(0x\x1b(B Andrew Anderson \x1b(0x\x1b(B andrew \x1b(0x\x1b(B\n\x1b(0mqqqqqqqqqqqqqqqqqvqqqqqqqqj\x1b(B\n'
