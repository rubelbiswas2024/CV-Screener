from typing import TypedDict
from langchain_core.documents import Document

class RAGState(TypedDict, total=False):
    question: str
    retrieved_documents: list[Document]
    answer: str
    sources: list[dict]