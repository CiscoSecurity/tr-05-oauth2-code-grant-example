from http import HTTPStatus
from unittest.mock import patch
import time


def test_oauth_successful_login(test_app):
    with test_app.test_client() as client:
        response = client.get('/login',
                              query_string={'region': 'North America'},
                              follow_redirects=False)
        assert response.status_code == HTTPStatus.FOUND


def test_oauth_login_with_exception(test_app):
    with test_app.test_client() as client:
        response = client.get('/login', follow_redirects=False)
        assert response.status_code == HTTPStatus.BAD_REQUEST


@patch('requests.request')
def test_oauth_successful_auth(mock_request, test_app,
                               tr_response, default_session):
    mock_request.return_value = tr_response(dict(expires_in=600))
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
        response = client.get('/auth',
                              query_string={'code': 123},
                              follow_redirects=False)
        assert response.status_code == HTTPStatus.FOUND


@patch('requests.request')
def test_oauth_successful_logout_with_update_tokens(mock_request,
                                                    test_app,
                                                    tr_response,
                                                    default_session):
    mock_request.return_value = tr_response(dict(expires_in=600))
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
            sess['oauth_token']['expires_at'] = time.time()
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code == HTTPStatus.FOUND
