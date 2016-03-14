import mock

from tests.support import config_values, config
from accountable.config import Config


class TestConfig(object):
    def test_creates_config_file(self, tmpdir):
        config(tmpdir, **config_values())
        assert len(tmpdir.listdir()) == 1

    @mock.patch.object(Config, '_load_config')
    @mock.patch.object(Config, '_initial_setup')
    def test_initial_setup(self, mock_method, mock_load, tmpdir):
        config(tmpdir, **config_values())
        mock_method.assert_called_once_with(config_values())

    @mock.patch.object(Config, '_load_config')
    def test_load_config(self, mock_method, tmpdir):
        config(tmpdir, **config_values())
        mock_method.assert_called_once_with()

    @mock.patch.object(Config, '_load_config')
    @mock.patch.object(Config, '_initial_setup')
    def test_does_not_setup(self,
                            mock_method,
                            mock_load,
                            tmpdir):
        config(tmpdir, **config_values())
        do_not_create_config = config_values().copy()
        del do_not_create_config['create_config']
        config(tmpdir, **do_not_create_config)
        mock_load.called_once_with(**config_values())
