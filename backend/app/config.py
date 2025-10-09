from __future__ import annotations
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://localhost/placeholder"
    secret_key: str
    frontend_origin: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    openai_api_key: str | None = None

    def callback_url(self) -> str:
        return f"{self.backend_url}/auth/callback"


def get_settings() -> Settings:
    # Map env -> settings names
    return Settings(
        database_url=os.environ.get("DATABASE_URL", ""),
        secret_key=os.environ["SECRET_KEY"],
        frontend_origin=os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000"),
        backend_url=os.environ.get("BACKEND_URL", "http://localhost:8000"),
        google_client_id=os.environ["GOOGLE_CLIENT_ID"],
        google_client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        google_redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )
