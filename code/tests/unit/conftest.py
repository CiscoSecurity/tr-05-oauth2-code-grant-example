from unittest.mock import MagicMock
from http import HTTPStatus
import time

import pytest

from app import app


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def tr_response():
    def _make_mock(payload=None, text=None, status_code=HTTPStatus.OK):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.ok = status_code == HTTPStatus.OK
        mock_response.json = lambda: payload
        mock_response.text = text
        return mock_response
    return _make_mock


@pytest.fixture(scope='module')
def default_session():
    return {
        'oauth_token': {
            'access_token': 'test_access_token',
            'expires_at': time.time() + 600,
            'refresh_token': 'test_refresh_token'
        },
        'region': 'North America'
    }
