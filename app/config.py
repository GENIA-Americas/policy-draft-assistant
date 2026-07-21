import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./policies.db")
    app_name: str = os.getenv("APP_NAME", "Policy Draft Assistant")


settings = Settings()
