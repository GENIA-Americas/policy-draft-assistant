from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_org
from app.clause_library import available_clauses, render_policy
from app.db import get_db
from app.models import PolicyDraft
from app.schemas import PolicyDraftCreate, PolicyDraftResult

router = APIRouter(tags=["policies"])


@router.get("/clauses/{policy_type}")
def list_clauses(policy_type: str, org_name: str = Depends(get_current_org)):
    clauses = available_clauses(policy_type)
    if not clauses:
        raise HTTPException(status_code=404, detail="Unknown policy type")
    return clauses


@router.post("/policies", response_model=PolicyDraftResult, status_code=201)
def create_policy_draft(
    payload: PolicyDraftCreate,
    db: Session = Depends(get_db),
    org_name: str = Depends(get_current_org),
):
    valid_keys = set(available_clauses(payload.policy_type).keys())
    unknown = [c for c in payload.selected_clauses if c not in valid_keys]
    if unknown:
        raise HTTPException(status_code=422, detail=f"Unknown clause keys: {unknown}")

    rendered_text = render_policy(org_name, payload.policy_type, payload.selected_clauses)

    record = PolicyDraft(
        org_name=org_name,
        policy_type=payload.policy_type,
        selected_clauses=payload.selected_clauses,
        rendered_text=rendered_text,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/policies/{draft_id}", response_model=PolicyDraftResult)
def get_policy_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    org_name: str = Depends(get_current_org),
):
    # Scoped to the caller's own org — a valid key for Org A must not be
    # able to read Org B's drafts by guessing/incrementing draft_id. This
    # returns the same 404 whether the draft doesn't exist at all or
    # belongs to someone else, so the endpoint doesn't leak which case it
    # is (that distinction is itself information).
    record = db.get(PolicyDraft, draft_id)
    if record is None or record.org_name != org_name:
        raise HTTPException(status_code=404, detail="Policy draft not found")
    return record
