"""Typed configuration for Mira, loaded from .env and environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root computed once at import time.
# settings.py → src/mira/ → src/ → mira-rebuild/  (three .parent calls)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """All configuration for the Mira project, loaded from .env."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ===== LLM Provider =====
    GROQ_API_KEY: str

    # ==== TELEGRAM ==========
    TELEGRAM_BOT_TOKEN: str

    # ===== Model Names =====
    TEXT_MODEL_NAME: str = "llama-3.3-70b-versatile"
    SMALL_TEXT_MODEL_NAME: str = "llama-3.1-8b-instant"

    # ===== Memory (short-term, SQLite) =====
    SHORT_TERM_MEMORY_DB_PATH: str = str(PROJECT_ROOT / "data" / "memory.db")

    # ===== Memory (long-term, Qdrant) =====
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "long_term_memory"
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"

settings = Settings()