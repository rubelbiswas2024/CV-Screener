import shutil
from app.config import get_settings, Settings
from app.ingestion.cv_loader import CVLoader
from app.ingestion.chunking import DocumentChunker
from app.RAG.embeddings_store import EmbeddingsProvider, VectorStoreManager


class IndexBuilder:
    """Rebuilds the CV vector index from the CV PDF directory."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Set up settings, loader, and chunker, or reuse the ones passed in."""
        self._settings = settings or get_settings()
        self._loader = CVLoader()
        self._chunker = DocumentChunker(self._settings)

    def rebuild(self) -> int:
        """Wipe the old index and rebuild it from the CV PDFs on disk."""
        documents = self._loader.load_directory(self._settings.cv_dir)

        if not documents:
            raise RuntimeError("No CV PDFs found.")

        chunks = self._chunker.split(documents)
        VectorStoreManager.clear()
        EmbeddingsProvider.clear()

        if self._settings.chroma_dir.exists():
            shutil.rmtree(self._settings.chroma_dir)

        store = VectorStoreManager.get()
        store.add_documents(chunks)

        return len(chunks)
