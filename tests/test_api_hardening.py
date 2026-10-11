
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.config import get_allowed_origins
from backend.api.main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_allowed_cors_origin():
    response = client.options(
        "/api/tasks",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )


def test_disallowed_cors_origin():
    response = client.options(
        "/api/tasks",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert (
        "access-control-allow-origin"
        not in response.headers
    )


def test_cors_wildcard_rejected():
    with patch.dict(
        "os.environ",
        {"CORS_ALLOWED_ORIGINS": "*"},
    ):
        try:
            get_allowed_origins()
            assert False, "Expected ValueError"
        except ValueError:
            pass


def test_unexpected_error_is_sanitized():
    with patch(
        "backend.api.routes.tasks.create_task",
        side_effect=RuntimeError(
            "Sensitive database connection details"
        ),
    ):
        response = client.post(
            "/api/tasks",
            json={
                "user_query": "Explain AWS EC2"
            },
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error."
    }
    assert (
        "Sensitive database connection details"
        not in response.text
    )


def test_query_exceeds_max_length():
    response = client.post(
        "/api/tasks",
        json={
            "user_query": "A" * 5001
        },
    )

    assert response.status_code == 422
