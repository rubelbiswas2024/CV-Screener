from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import get_settings, Settings


class DocumentChunker:
    """Splits loaded CV documents into overlapping text chunks for embedding."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Load settings needed for chunk size, or reuse the ones passed in."""
        self._settings = settings or get_settings()

    def split(self, documents: list[Document]) -> list[Document]:
        """Split documents into overlapping chunks sized for embedding."""
        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=(self._settings.chunk_size), chunk_overlap=(self._settings.chunk_overlap_size),
                separators=["\n\n", "\n", ". ", " ", ""],
            )
        )

        return splitter.split_documents(documents)
