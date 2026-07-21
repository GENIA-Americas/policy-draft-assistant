# policy-draft-assistant

Part of the GENIA Americas AI Toolkit — repo #7. Assembles AI governance policy drafts
from a fixed clause library.

**Honest scope note:** this is a deterministic template engine — it assembles pre-written
clauses you select, it does not call an LLM to generate novel policy language. If you want
actual generative drafting, that would mean integrating a real model call (e.g. the
Anthropic API) on top of this, which is not built here.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run
```bash
uvicorn app.main:app --reload
```
Docs at http://127.0.0.1:8000/docs

## Test
```bash
pytest tests/ -v
```
11/11 tests pass as of last verified run.

## Auth
All endpoints require an `X-API-Key` header. Keys are configured via the `API_KEYS`
env var as `key1:org_one,key2:org_two` — each key authenticates its caller as exactly
one org, and reads/writes are scoped to that org (a valid key for one org cannot read
another org's drafts).

## API
- `GET /clauses/{policy_type}` — list available clause keys/text for a policy type
  (`acceptable_use`, `data_governance`, `vendor_risk`).
- `POST /policies` — submit policy type and selected clause keys; org name is derived
  from your API key, not sent in the request body. Get back the assembled policy text.
- `GET /policies/{id}` — retrieve one draft belonging to your org.
- `GET /health`

## Extending the clause library
Add entries to `app/clause_library.py`. Legal/compliance review of any clause before real
use is your responsibility — this tool assembles text, it doesn't validate legal accuracy.
