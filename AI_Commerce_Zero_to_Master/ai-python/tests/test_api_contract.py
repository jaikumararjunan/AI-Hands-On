import os

from fastapi.testclient import TestClient

from app.main import app, agent_service


def test_openapi_document_has_supported_version_and_agent_path():
    document = app.openapi()
    assert str(document.get("openapi", "")).startswith("3.")
    assert "/ai/agent/ask" in document.get("paths", {})


def test_fastapi_root_path_is_configurable_for_reverse_proxy():
    expected = os.getenv("FASTAPI_ROOT_PATH", "")
    assert app.root_path == expected


def test_agent_endpoint_accepts_question_json(monkeypatch):
    monkeypatch.setattr(
        agent_service,
        "ask",
        lambda question: {"route": "search", "answer": f"accepted:{question}", "degraded": False},
    )
    client = TestClient(app)
    response = client.post(
        "/ai/agent/ask",
        json={"question": "I need a laptop for local AI development and a monitor"},
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["route"] == "search"
    assert payload["degraded"] is False
    assert "laptop" in payload["answer"].lower()


def test_agent_endpoint_rejects_invalid_body_with_explainable_422():
    client = TestClient(app)
    response = client.post("/ai/agent/ask", json={"wrongField": "hello"})
    assert response.status_code == 422
    detail = response.json().get("detail", [])
    assert detail
