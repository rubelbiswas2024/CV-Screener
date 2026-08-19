from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from app.config import get_settings


class EmbeddingsProvider:
    """Provides a cached singleton embeddings model."""

    _instance = None

    @classmethod
    def get(cls) -> FastEmbedEmbeddings:
        """Return the shared embeddings model, creating it on first use."""
        if cls._instance is None:
            settings = get_settings()
            cls._instance = FastEmbedEmbeddings(model_name=settings.embedding_model)
        return cls._instance

    @classmethod
    def clear(cls) -> None:
        """Drop the cached embeddings model so the next get() rebuilds it."""
        cls._instance = None


class VectorStoreManager:
    """Provides a cached singleton Chroma vector store backed by the configured directory."""

    _instance = None

    @classmethod
    def get(cls) -> Chroma:
        """Return the shared Chroma store, creating it on first use."""
        if cls._instance is None:
            settings = get_settings()
            settings.chroma_dir.mkdir(parents=True, exist_ok=True)

            cls._instance = Chroma(
                collection_name="cv_chunks",
                embedding_function=EmbeddingsProvider.get(),
                persist_directory=str(settings.chroma_dir),
            )
        return cls._instance

    @classmethod
    def clear(cls) -> None:
        """Drop the cached vector store so the next get() rebuilds it."""
        cls._instance = None
