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

    @mock.patch('accountable.accountable.Resource.post')
    @mock.patch('accountable.accountable.Resource.get')
    def test_checkoutbranch(self, mock_get, mock_post, tmpdir):
        mock_post.return_value = support.issue_create()
        mock_get.return_value = support.metadata_response()
        a = support.accountable(tmpdir)
        a._repo = mock.MagicMock(name='_repo')
        a.checkout_branch(('summary', 'slug me',
                           'project.id', '1'))
        a._repo.return_value.checkout.assert_called_once_with(
            u'HEAD', b=u'TST-24-slug-me'
        )
