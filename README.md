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
7/7 tests pass as of last verified run.

## API
- `GET /clauses/{policy_type}` — list available clause keys/text for a policy type
  (`acceptable_use`, `data_governance`, `vendor_risk`).
- `POST /policies` — submit org name, policy type, and selected clause keys; get back the
  assembled policy text.
- `GET /policies/{id}` — retrieve one draft.
- `GET /health`

## Extending the clause library
Add entries to `app/clause_library.py`. Legal/compliance review of any clause before real
use is your responsibility — this tool assembles text, it doesn't validate legal accuracy.
