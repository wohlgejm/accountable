import pytest

from accountable.accountable import Accountable


def config_values():
    return {
        'username': 'testusername',
        'password': 'testpassword',
        'domain': 'testdomain',
        'create_config': True,
    }


def metadata_response():
    return {

    }


@pytest.fixture
def accountable(tmpdir, **kwargs):
    Accountable.CONFIG_DIR = '{}/.accountable'.format(str(tmpdir))
    Accountable.CONFIG_FILE = '{}/config.yaml'.format(Accountable.CONFIG_DIR)
    return Accountable(**kwargs)
