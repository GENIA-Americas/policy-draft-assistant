from fastapi import FastAPI

from app.config import settings
from app.db import Base, engine
from app.routers import policies

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description=(
        "Assembles AI governance policy drafts from a fixed clause library. "
        "Deterministic template engine, not a generative model call."
    ),
    version="0.1.0",
)

app.include_router(policies.router)


@app.get("/health")
def health():
    return {"status": "ok"}
