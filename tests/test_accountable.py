from __future__ import absolute_import

import mock

from accountable.accountable import Accountable
from tests.support import config_values, accountable


class TestAccountable(object):
    def test_creates_config_file(self, tmpdir):
        accountable(tmpdir, **config_values())
        assert len(tmpdir.listdir()) == 1

    @mock.patch.object(Accountable, '_load_config')
    @mock.patch.object(Accountable, '_initial_setup')
    def test_initial_setup(self, mock_method, mock_load, tmpdir):
        accountable(tmpdir, **config_values())
        mock_method.assert_called_once_with()

    @mock.patch.object(Accountable, '_load_config')
    def test_load_config(self, mock_method, tmpdir):
        accountable(tmpdir, **config_values())
        mock_method.assert_called_once_with()

    @mock.patch.object(Accountable, '_load_config')
    @mock.patch.object(Accountable, '_initial_setup')
    def test_does_not_setup_if_create_not_specified(self,
                                                    mock_method,
                                                    mock_load,
                                                    tmpdir):
        accountable(tmpdir, **config_values())
        do_not_create_config = config_values().copy()
        del do_not_create_config['create_config']
        accountable(tmpdir, **do_not_create_config)
        mock_method.assert_called_once_with()
