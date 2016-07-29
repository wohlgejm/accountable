from __future__ import absolute_import

import mock

from tests import support


class TestAccountable(object):
    @mock.patch('accountable.accountable.Resource.get')
    def test_projects(self, mock_object, tmpdir):
        a = support.accountable(tmpdir)
        mock_object.return_value = support.metadata_response()
        assert a.projects() == [('10000', 'EX', 'Example Project'),
                                ('10000', 'AC', 'Accountable')]

    @mock.patch('accountable.accountable.Resource.get')
    def test_all_issuetypes(self, mock_object, tmpdir):
        a = support.accountable(tmpdir)
        mock_object.return_value = support.metadata_response()
        assert set(list(a.issue_types('').keys())) == set(['EX', 'AC'])

    @mock.patch('accountable.accountable.Resource.get')
    def test_single_issuetypes(self, mock_object, tmpdir):
        a = support.accountable(tmpdir)
        mock_object.return_value = support.metadata_response()
        assert list(a.issue_types('EX').keys()) == ['EX']
