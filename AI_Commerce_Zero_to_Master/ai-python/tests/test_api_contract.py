from fastapi.testclient import TestClient

from app.main import app, agent_service


def test_openapi_document_has_supported_version_and_agent_path():
    document = app.openapi()
    assert str(document.get("openapi", "")).startswith("3.")
    assert "/ai/agent/ask" in document.get("paths", {})


def test_direct_swagger_uses_direct_openapi_path():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
    assert "url: '/openapi.json'" in response.text


def test_proxied_swagger_honors_forwarded_prefix():
    client = TestClient(app)
    response = client.get("/docs", headers={"X-Forwarded-Prefix": "/python"})
    assert response.status_code == 200
    assert "url: '/python/openapi.json'" in response.text


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
