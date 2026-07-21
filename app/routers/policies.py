from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.clause_library import available_clauses, render_policy
from app.db import get_db
from app.models import PolicyDraft
from app.schemas import PolicyDraftCreate, PolicyDraftResult

router = APIRouter(tags=["policies"])


@router.get("/clauses/{policy_type}")
def list_clauses(policy_type: str):
    clauses = available_clauses(policy_type)
    if not clauses:
        raise HTTPException(status_code=404, detail="Unknown policy type")
    return clauses


@router.post("/policies", response_model=PolicyDraftResult, status_code=201)
def create_policy_draft(payload: PolicyDraftCreate, db: Session = Depends(get_db)):
    valid_keys = set(available_clauses(payload.policy_type).keys())
    unknown = [c for c in payload.selected_clauses if c not in valid_keys]
    if unknown:
        raise HTTPException(status_code=422, detail=f"Unknown clause keys: {unknown}")

    rendered_text = render_policy(payload.org_name, payload.policy_type, payload.selected_clauses)

    record = PolicyDraft(
        org_name=payload.org_name,
        policy_type=payload.policy_type,
        selected_clauses=payload.selected_clauses,
        rendered_text=rendered_text,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/policies/{draft_id}", response_model=PolicyDraftResult)
def get_policy_draft(draft_id: int, db: Session = Depends(get_db)):
    record = db.get(PolicyDraft, draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Policy draft not found")
    return record
