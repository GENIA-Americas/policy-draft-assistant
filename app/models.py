from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class PolicyDraft(Base):
    __tablename__ = "policy_drafts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_name: Mapped[str] = mapped_column(String, index=True)
    policy_type: Mapped[str] = mapped_column(String)  # "acceptable_use" | "data_governance" | "vendor_risk"
    selected_clauses: Mapped[list] = mapped_column(JSON)
    rendered_text: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
