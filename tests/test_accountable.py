from __future__ import absolute_import

import mock

from tests.support import config_values, accountable, metadata_response


class TestAccountable(object):
    @mock.patch('accountable.jira.Jira.metadata')
    def test_projects(self, mock_object, tmpdir):
        a = accountable(tmpdir, **config_values())
        mock_object.return_value = metadata_response()
        assert a.projects() == [('EX', 'Example Project'),
                                ('AC', 'Accountable')]

    @mock.patch('accountable.jira.Jira.metadata')
    def test_all_issuetypes(self, mock_object, tmpdir):
        a = accountable(tmpdir, **config_values())
        mock_object.return_value = metadata_response()
        assert set(list(a.issue_types('').keys())) == set(['EX', 'AC'])

    @mock.patch('accountable.jira.Jira.metadata')
    def test_single_issuetypes(self, mock_object, tmpdir):
        a = accountable(tmpdir, **config_values())
        mock_object.return_value = metadata_response()
        assert list(a.issue_types('EX').keys()) == ['EX']

    def test_issue_meta(self):
        pass
