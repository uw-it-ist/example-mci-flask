from unittest.mock import patch

import os
os.environ['FLASK_SESSION_KEY'] = 'abc123'
os.environ['DSN_TOOLSDB'] = 'host=localhost user=toolop dbname=ripit_2 sslmode=require'

# monkey patch flask_caching to work without redis during testing
from flask_caching import Cache  # noqa: E402
import flask_app.app  # noqa: E402
flask_app.app.cache = Cache(config={
    "CACHE_TYPE": "simple",
})

app = flask_app.app.load()


def test_health_check():
    with app.test_client() as c:
        rv = c.get(path='/healthz')
        assert b'OK' in rv.data and rv.status_code == 200


def test_api_health_check():
    with app.test_client() as c:
        rv = c.get(path='/api/healthz')
        assert b'{"pass":true}' in rv.data and rv.status_code == 200


def test_index_page_401():
    with app.test_client() as c:
        rv = c.get(path='/')
        assert rv.status_code == 401


def test_item_page_401():
    with app.test_client() as c:
        rv = c.get(path='/item/1')
        assert rv.status_code == 401


def test_item_page():
    app.testing = True
    test_auth_header = {'X-Forwarded-User': 'test-user'}
    with app.test_client() as c:
        rv = c.get(headers=test_auth_header, path='/item/1')
        assert b'This is item id' in rv.data and rv.status_code == 200


def test_db_down():
    app.testing = True
    test_auth_header = {'X-Forwarded-User': 'test-user'}
    with app.test_client() as c:
        rv = c.get(headers=test_auth_header, path='/')
        assert b'Unable to connect to database' in rv.data and rv.status_code == 500


@patch("psycopg2.connect")
def test_index_page(mock_connect):
    expected = [{'id': 1, 'name': 'foo'}, {'id': 2, 'name': 'bar'}]
    mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
    app.testing = True
    test_auth_header = {'X-Forwarded-User': 'test-user'}
    with app.test_client() as c:
        rv = c.get(headers=test_auth_header, path='/')
        assert b'core-content-container' in rv.data and rv.status_code == 200


def test_saml_groups():
    app.testing = True
    test_auth_header = {
        'X-Forwarded-User': 'test-user',
        'X-Forwarded-Groups': 'group1:group2'
        }
    with app.test_client() as c:
        rv = c.get(headers=test_auth_header, path='/item/1')
        assert b'This is item id' in rv.data and rv.status_code == 200
