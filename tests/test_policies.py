import os

os.environ["DATABASE_URL"] = "sqlite:///./test_policies.db"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_list_clauses_for_valid_type():
    resp = client.get("/clauses/acceptable_use")
    assert resp.status_code == 200
    assert "no_confidential_input" in resp.json()


def test_list_clauses_for_unknown_type_404():
    assert client.get("/clauses/not_a_real_type").status_code == 404


def test_create_policy_draft():
    payload = {
        "org_name": "Acme Test Co",
        "policy_type": "acceptable_use",
        "selected_clauses": ["no_confidential_input", "human_review_required"],
    }
    resp = client.post("/policies", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert "no_confidential_input" not in body["rendered_text"]  # key isn't in text, its value is
    assert "confidential" in body["rendered_text"].lower()


def test_rejects_unknown_clause_key():
    payload = {
        "org_name": "Acme Test Co",
        "policy_type": "acceptable_use",
        "selected_clauses": ["not_a_real_clause"],
    }
    resp = client.post("/policies", json=payload)
    assert resp.status_code == 422


def test_get_policy_draft():
    payload = {
        "org_name": "Acme Test Co",
        "policy_type": "data_governance",
        "selected_clauses": ["data_minimization"],
    }
    created = client.post("/policies", json=payload).json()
    resp = client.get(f"/policies/{created['id']}")
    assert resp.status_code == 200


def test_missing_policy_draft_404():
    assert client.get("/policies/999999").status_code == 404
