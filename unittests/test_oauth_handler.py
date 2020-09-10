import time

import pytest
from flask import session

from oauth_handler import OAuth2CTR

TEST_TOKENS = {'access_token': 'test_access_token',
               'refresh_token': 'test_refresh_token',
               'token_type': 'bearer', 'expires_in': 600, 'scope': 'integration admin inspect'}


@pytest.fixture
def mock_state(monkeypatch):
    monkeypatch.setattr(OAuth2CTR, "_generate_state", lambda *args, **kwargs: "mocked_state")


@pytest.fixture
def mock_time(monkeypatch):
    monkeypatch.setattr(time, "time", lambda *args, **kwargs: 1500000000)


def test_oauth_authorization_url(test_app, mock_state):
    with test_app.test_request_context():
        auth = OAuth2CTR()
        url = auth.get_authorization_url()

        assert url == "https://visibility.amp.cisco.com/iroh/oauth2/" \
                      "authorize?response_type=code&client_id=test_id&" \
                      "redirect_uri=http%3A%2F%2Flocalhost%2Fauth&" \
                      "scope=admin+integration+inspect&" \
                      "state=mocked_state"


def test_oauth_get_tokens_expiration_time(test_app, mock_time):
    with test_app.test_request_context():
        auth = OAuth2CTR()
        expires_at = auth._get_tokens_expiration_time(expires_in=600)

        assert expires_at == 1500000600


def test_oauth_save_token(test_app, mock_time):
    with test_app.test_request_context():
        auth = OAuth2CTR()
        auth._save_tokens(dict(TEST_TOKENS))

        assert session["oauth_token"] == {'access_token': 'test_access_token',
                                          'refresh_token': 'test_refresh_token',
                                          'token_type': 'bearer', 'expires_in': 600,
                                          'expires_at': 1500000600,
                                          'scope': 'integration admin inspect'}
