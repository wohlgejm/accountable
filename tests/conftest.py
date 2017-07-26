from __future__ import absolute_import

import json

import pytest
import requests
from doubles import allow

from tests import fixtures


class MockResponse(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return json.loads(json.dumps(self.data, allow_nan=False))

    def status_code(self):
        return self.status_code


@pytest.fixture
def get_issue():
    response = MockResponse(200, fixtures.issue)
    allow(requests).get.and_return(response)
