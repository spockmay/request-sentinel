import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_logs_endpoint(client):
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_request_is_logged(client, app):
    client.get("/")
    with app.app_context():
        from app.models.request_log import RequestLog

        logs = RequestLog.query.all()
        assert len(logs) >= 1
        assert logs[0].path == "/"
