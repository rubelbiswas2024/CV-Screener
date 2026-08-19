from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env files."""

    anthropic_api_key: str
    llm_model: str = "claude-opus-5"

    image_model: str = "flux"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    cv_dir: Path = Path("./data/resumes")
    candidate_dir: Path = Path("./data/candidates")
    image_dir: Path = Path("./data/photos")
    chroma_dir: Path = Field(default=Path("./data/databases"), alias="DATABASE_DIR")



    chunk_size: int = 900
    chunk_overlap_size: int = 150
    top_k: int = 8


    log_level:str = "INFO"


    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """App settings: the lru_cache decorator confirms the Settings object is created only once and reused."""
    return Settings()
