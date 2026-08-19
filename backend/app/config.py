from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env files.

    Contains settings for OpenRouter models, resumes and candidate data directories,
    vector database, document chunking, retrieval, and logging.
    """

    anthropic_api_key: str
    llm_model: str = "claude-opus-5"

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    image_model: str = "google/gemini-3.1-flash-lite-image"

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
    """
    App settings: The lru_cache decorator confirms that the Settings object is created
    only once and the same instance is reused throughout the app.
    """
    return Settings()
