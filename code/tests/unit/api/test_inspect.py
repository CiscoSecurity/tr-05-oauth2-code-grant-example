from http import HTTPStatus
from unittest.mock import patch


@patch('requests.request')
def test_oauth_successful_auth(mock_request, test_app,
                               tr_response, default_session):
    inspected_observable = [
        {
            'value': '8.8.8.8',
            'type': 'ip'
        }
    ]
    mock_request.return_value = tr_response(inspected_observable)
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
        response = client.post('/inspect', query_string={'content': '8.8.8.8'})
        assert response.status_code == HTTPStatus.OK
