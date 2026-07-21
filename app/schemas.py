from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PolicyType = Literal["acceptable_use", "data_governance", "vendor_risk"]


class PolicyDraftCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    org_name: str = Field(min_length=1, max_length=200)
    policy_type: PolicyType
    selected_clauses: list[str] = Field(min_length=1)


class PolicyDraftResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    org_name: str
    policy_type: str
    selected_clauses: list[str]
    rendered_text: str
    created_at: datetime
