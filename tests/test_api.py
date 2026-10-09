from fastapi.testclient import TestClient
import pytest
from fastapi.exceptions import ResponseValidationError
from app import main

client = TestClient(main.app)
KEYS = {"status", "answer", "citations", "handoff"}


def fake(status, **extra):
    base = {"status": status, "answer": "x", "citations": [], "handoff": None}
    base.update(extra)
    return lambda sid, msg: base


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_chat_schema_answered(monkeypatch):
    cite = {"title": "T", "url": "https://u", "section": None}
    monkeypatch.setattr(main.pipeline, "handle", fake("answered", citations=[cite]))
    r = client.post("/chat", json={"session_id": "s", "message": "hi there"})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == KEYS and body["status"] == "answered"
    assert set(body["citations"][0]) == {"title", "url", "section"}


def test_chat_handoff_shape(monkeypatch):
    h = {"summary": "s", "intent": "i", "articles_tried": ["https://u"]}
    monkeypatch.setattr(main.pipeline, "handle", fake("handoff", handoff=h))
    body = client.post("/chat", json={"session_id": "s", "message": "human"}).json()
    assert set(body["handoff"]) == {"summary", "intent", "articles_tried"}


def test_non_handoff_has_null_handoff(monkeypatch):
    monkeypatch.setattr(main.pipeline, "handle", fake("clarify"))
    assert client.post("/chat", json={"session_id": "s", "message": "help"}).json()["handoff"] is None


def test_empty_message_rejected():
    assert client.post("/chat", json={"session_id": "s", "message": ""}).status_code == 422


def test_missing_session_rejected():
    assert client.post("/chat", json={"message": "hello"}).status_code == 422


def test_pipeline_crash_returns_safe_json(monkeypatch):
    def boom(sid, msg):
        raise RuntimeError("x")
    monkeypatch.setattr(main.pipeline, "handle", boom)
    r = client.post("/chat", json={"session_id": "s", "message": "hello"})
    assert r.status_code == 200 and r.json()["status"] == "out_of_scope"




def test_invalid_status_degrades_to_safe_refusal(monkeypatch):
    monkeypatch.setattr(main.pipeline, "handle", fake("weird"))
    r = client.post("/chat", json={"session_id": "s", "message": "hello"})
    assert r.status_code == 200
    assert r.json()["status"] == "out_of_scope"