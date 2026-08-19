from types import SimpleNamespace

from langchain_core.documents import Document

from app.ingestion.chunking import DocumentChunker


def _chunker(chunk_size: int, chunk_overlap_size: int) -> DocumentChunker:
    fake_settings = SimpleNamespace(chunk_size=chunk_size, chunk_overlap_size=chunk_overlap_size)
    return DocumentChunker(settings=fake_settings)


def test_split_breaks_a_long_document_into_multiple_chunks():
    long_text = "word " * 500
    document = Document(page_content=long_text, metadata={"source": "C001.pdf"})

    chunks = _chunker(chunk_size=200, chunk_overlap_size=20).split([document])

    assert len(chunks) > 1
    assert all(chunk.metadata["source"] == "C001.pdf" for chunk in chunks)


def test_split_keeps_a_short_document_as_one_chunk():
    document = Document(page_content="Short CV summary.", metadata={"source": "C002.pdf"})

    chunks = _chunker(chunk_size=900, chunk_overlap_size=150).split([document])

    assert len(chunks) == 1
    assert chunks[0].page_content == "Short CV summary."
