from http import HTTPStatus
from unittest.mock import patch


@patch('requests.request')
def test_modules_successful_get_modules(mock_request, test_app,
                                        tr_response, default_session):
    modules = [
        {
            'name': 'Module1',
            'id': '07114c0b-06bc-4d79-8e12-1a5f234565fd',
        },
        {
            'name': 'Module2',
            'id': '0a5738eb-934e-3719-92cd-fb4d2a60e9b2',
        }
    ]
    mock_request.return_value = tr_response(modules)
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
        response = client.get('/modules')
        assert 'Module1' in str(response.data)
        assert 'Module2' in str(response.data)
        assert response.status_code == HTTPStatus.OK


def test_modules_get_modules_not_logged_in(test_app):
    with test_app.test_client() as client:
        response = client.get('/modules')
        assert response.status_code == HTTPStatus.OK
        assert 'You have not login yet :(' in str(response.data)


@patch('requests.request')
def test_modules_create_module(mock_request, test_app,
                               tr_response, default_session):
    created_module = {
        'name': 'NewModule',
        'id': '07114c0b-06bc-4d79-8e12-1a5f234565fd',
        }
    mock_request.return_value = tr_response(created_module)
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
        response = client.post('/modules', query_string={'name': 'NewModule'})
        assert response.status_code == HTTPStatus.OK
        assert 'NewModule' in str(response.data)


@patch('requests.request')
def test_modules_delete_module(mock_request, test_app,
                               tr_response, default_session):
    mock_request.return_value = tr_response({})
    with test_app.test_client() as client:
        with client.session_transaction() as sess:
            sess.update(default_session)
        response = client.get('/modules/delete',
                              query_string={'module_id': 123})
        assert response.status_code == HTTPStatus.OK
        assert 'Successfully deleted module with ID 123' in str(response.data)
