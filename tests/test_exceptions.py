import pytest

from apiflask.exceptions import abort
from apiflask.exceptions import HTTPError


@pytest.mark.parametrize(
    'kwargs',
    [
        {},
        {'message': 'bad'},
        {'message': 'bad', 'detail': {'location': 'json'}},
        {'message': 'bad', 'detail': {'location': 'json'}, 'headers': {'X-FOO': 'bar'}},
    ],
)
def test_httperror(app, client, kwargs):
    @app.get('/foo')
    def foo():
        raise HTTPError(400, **kwargs)

    @app.get('/bar')
    def bar():
        raise HTTPError

    rv = client.get('/foo')
    assert rv.status_code == 400
    if 'message' not in kwargs:
        assert rv.json['message'] == 'Bad Request'
    else:
        assert rv.json['message'] == 'bad'
    if 'detail' not in kwargs:
        assert rv.json['detail'] == {}
    else:
        assert rv.json['detail'] == {'location': 'json'}
    if 'headers' in kwargs:
        assert rv.headers['X-FOO'] == 'bar'

    # test default error status code
    rv = client.get('/bar')
    assert rv.status_code == 500
    assert rv.json['message'] == 'Internal Server Error'
    assert rv.json['detail'] == {}


@pytest.mark.parametrize(
    'kwargs',
    [
        {},
        {'message': 'missing'},
        {'message': 'missing', 'detail': {'location': 'query'}},
        {'message': 'missing', 'detail': {'location': 'query'}, 'headers': {'X-BAR': 'foo'}},
        {'message': 'missing', 'extra_data': {'code': 123, 'status': 'not_found'}},
    ],
)
def test_abort(app, client, kwargs):
    @app.get('/bar')
    def bar():
        abort(404, **kwargs)

    rv = client.get('/bar')
    assert rv.status_code == 404
    if 'message' not in kwargs:
        assert rv.json['message'] == 'Not Found'
    else:
        assert rv.json['message'] == 'missing'
    if 'detail' not in kwargs:
        assert rv.json['detail'] == {}
    else:
        assert rv.json['detail'] == {'location': 'query'}
    if 'headers' in kwargs:
        assert rv.headers['X-BAR'] == 'foo'
    if 'extra_data' in kwargs:
        assert rv.json['code'] == 123
        assert rv.json['status'] == 'not_found'


@pytest.mark.parametrize(
    'kwargs',
    [
        {},
        {'message': 'bad'},
        {'message': 'bad', 'detail': {'location': 'json'}},
        {'message': 'bad', 'detail': {'location': 'json'}, 'headers': {'X-FOO': 'bar'}},
    ],
)
def test_default_error_handler(app, kwargs):
    error = HTTPError(400, **kwargs)
    rv = app._error_handler(error)
    assert rv[1] == 400
    if 'message' not in kwargs:
        assert rv[0]['message'] == 'Bad Request'
    else:
        assert rv[0]['message'] == 'bad'
    if 'detail' not in kwargs:
        assert rv[0]['detail'] == {}
    else:
        assert rv[0]['detail'] == {'location': 'json'}
    if 'headers' in kwargs:
        assert rv[2]['X-FOO'] == 'bar'


def test_invalid_error_status_code():
    with pytest.raises(LookupError):
        abort(200)

    with pytest.raises(LookupError):
        raise HTTPError(204)


def test_custom_error_classes(app, client):
    class PetDown(HTTPError):
        status_code = 400
        message = 'The pet is down.'
        extra_data = {'error_code': '123', 'error_docs': 'https://example.com/docs/down'}
        headers = {'X-Foo': 'bar'}

    class PetNotFound(HTTPError):
        status_code = 404
        message = 'The pet is gone.'
        extra_data = {'error_code': '345', 'error_docs': 'https://example.com/docs/gone'}

    @app.get('/foo')
    def foo():
        raise PetDown

    @app.get('/bar')
    def bar():
        raise PetNotFound

    rv = client.get('/foo')
    assert rv.status_code == 400
    assert rv.json['message'] == 'The pet is down.'
    assert rv.json['error_code'] == '123'
    assert rv.json['error_docs'] == 'https://example.com/docs/down'
    assert rv.json['detail'] == {}
    assert rv.headers['X-FOO'] == 'bar'

    rv = client.get('/bar')
    assert rv.status_code == 404
    assert rv.json['message'] == 'The pet is gone.'
    assert rv.json['error_code'] == '345'
    assert rv.json['error_docs'] == 'https://example.com/docs/gone'
    assert rv.json['detail'] == {}
