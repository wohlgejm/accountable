import mock

from accountable.accountable import Accountable


def config_values():
    return {
        'username': 'testusername',
        'password': 'testpassword',
        'domain': 'testdomain',
        'create_config': True,
    }


class TestAccountable(object):
    @mock.patch.object(Accountable, '_initial_setup')
    def test_initial_setup(self, mock_method, tmpdir):
        Accountable.CONFIG_DIR = str(tmpdir)
        Accountable(**config_values())
        mock_method.assert_called_once_with()

    @mock.patch.object(Accountable, '_load_config')
    def test_load_config(self, mock_method, tmpdir):
        Accountable.CONFIG_DIR = str(tmpdir)
        Accountable(**config_values())
        mock_method.assert_called_once_with()

    @mock.patch.object(Accountable, '_initial_setup')
    def test_does_not_setup_if_config_exists(self, mock_method, tmpdir):
        Accountable.CONFIG_DIR = str(tmpdir)
        Accountable(**config_values())
        do_not_create_config = config_values().copy()
        del do_not_create_config['create_config']
        Accountable(**do_not_create_config)
        mock_method.assert_called_once_with()
