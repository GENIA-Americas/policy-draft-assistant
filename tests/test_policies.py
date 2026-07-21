import os

os.environ["DATABASE_URL"] = "sqlite:///./test_policies.db"
os.environ["API_KEYS"] = "devkey1:acme_corp,devkey2:globex_inc"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ACME_HEADERS = {"X-API-Key": "devkey1"}
GLOBEX_HEADERS = {"X-API-Key": "devkey2"}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_list_clauses_requires_api_key():
    resp = client.get("/clauses/acceptable_use")
    assert resp.status_code == 401


def test_list_clauses_rejects_invalid_api_key():
    resp = client.get("/clauses/acceptable_use", headers={"X-API-Key": "not-a-real-key"})
    assert resp.status_code == 401


def test_list_clauses_for_valid_type():
    resp = client.get("/clauses/acceptable_use", headers=ACME_HEADERS)
    assert resp.status_code == 200
    assert "no_confidential_input" in resp.json()


def test_list_clauses_for_unknown_type_404():
    resp = client.get("/clauses/not_a_real_type", headers=ACME_HEADERS)
    assert resp.status_code == 404


def test_create_policy_draft():
    payload = {
        "policy_type": "acceptable_use",
        "selected_clauses": ["no_confidential_input", "human_review_required"],
    }
    resp = client.post("/policies", json=payload, headers=ACME_HEADERS)
    assert resp.status_code == 201
    body = resp.json()
    assert body["org_name"] == "acme_corp"  # derived from the API key, not client input
    assert "no_confidential_input" not in body["rendered_text"]  # key isn't in text, its value is
    assert "confidential" in body["rendered_text"].lower()


def test_create_policy_draft_requires_api_key():
    payload = {
        "policy_type": "acceptable_use",
        "selected_clauses": ["no_confidential_input"],
    }
    resp = client.post("/policies", json=payload)
    assert resp.status_code == 401


def test_rejects_unknown_clause_key():
    payload = {
        "policy_type": "acceptable_use",
        "selected_clauses": ["not_a_real_clause"],
    }
    resp = client.post("/policies", json=payload, headers=ACME_HEADERS)
    assert resp.status_code == 422


def test_get_policy_draft():
    payload = {
        "policy_type": "data_governance",
        "selected_clauses": ["data_minimization"],
    }
    created = client.post("/policies", json=payload, headers=ACME_HEADERS).json()
    resp = client.get(f"/policies/{created['id']}", headers=ACME_HEADERS)
    assert resp.status_code == 200


def test_cannot_read_another_orgs_policy_draft():
    payload = {
        "policy_type": "data_governance",
        "selected_clauses": ["data_minimization"],
    }
    created = client.post("/policies", json=payload, headers=ACME_HEADERS).json()
    # Globex has a valid key, just not for this draft — must not be able to
    # read Acme's draft by guessing/incrementing the id.
    resp = client.get(f"/policies/{created['id']}", headers=GLOBEX_HEADERS)
    assert resp.status_code == 404


def test_missing_policy_draft_404():
    resp = client.get("/policies/999999", headers=ACME_HEADERS)
    assert resp.status_code == 404
