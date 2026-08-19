from app.RAG.graph import RAGPipeline, graph as default_pipeline


class ChatService:
    """Wraps the RAG pipeline for use by the API layer."""

    def __init__(self, pipeline: RAGPipeline | None = None) -> None:
        self._pipeline = pipeline or default_pipeline

    def ask(self, question: str) -> dict:
        """Run a question through the RAG pipeline and return the answer with sources."""
        return self._pipeline.invoke({"question": question})
