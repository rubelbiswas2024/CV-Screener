import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from app.config import get_settings, Settings
from app.RAG.rag_prompts import SYSTEM_PROMPT
from app.RAG.state import RAGState
from app.RAG.embeddings_store import VectorStoreManager
from app.ingestion.chunk_indexing import IndexBuilder


logger = logging.getLogger(__name__)


class RAGPipeline:
    """Retrieval-augmented generation pipeline over the CV vector store."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Set up settings, the LLM client, and the compiled retrieve/generate graph."""
        self._settings = settings or get_settings()
        self._llm = ChatAnthropic(model=self._settings.llm_model, api_key=self._settings.anthropic_api_key)
        self._graph = self._build_graph()

    def _retrieve(self, state: RAGState) -> dict:
        """Fetch the top matching CV chunks for the question, building the index first if it's missing."""
        store = VectorStoreManager.get()

        if not store.get(limit=1)["ids"]:
            logger.info("event=index_missing action=building")
            IndexBuilder(self._settings).build_if_missing()

        documents = store.similarity_search(state["question"], k=self._settings.top_k)
        logger.info("event=retrieval " "chunks=%s ", len(documents))

        return {"retrieved_documents": documents}

    def _generate(self, state: RAGState) -> dict:
        """Answer the question from the retrieved chunks and list the sources used."""

        context_blocks = []
        documents = state.get("retrieved_documents", [])

        if not documents:
            return {"answer": ("I could not find relevant information in the CV collection."),
                "sources": []
            }

        for index, document in enumerate(documents, start=1):
            metadata = document.metadata
            context_blocks.append((f"[SOURCE {index}]\n" f"Candidate: " f"{metadata.get('candidate_name')}\n"
                    f"CV: " f"{metadata.get('source')}\n" f"Page: " f"{metadata.get('page')}\n\n"
                    f"{document.page_content}"
                )
            )
        context = "\n\n".join(context_blocks)

        prompt = f"""CV CONTEXT {context} QUESTION {state["question"]}"""
        response = self._llm.invoke([SystemMessage(content=SYSTEM_PROMPT,), HumanMessage(
                    content=prompt
                ),
            ]
        )

        logger.info("event=llm_generation ")
        unique_sources = []
        seen = set()

        for document in documents:
            metadata = document.metadata
            key = (metadata.get("source"), metadata.get("page"))
            if key in seen:
                continue
            seen.add(key)
            unique_sources.append(
                {
                    "candidate_id": metadata.get("candidate_id", ""),
                    "candidate_name": metadata.get("candidate_name", ""),
                    "file": metadata.get("source", ""),
                    "page": metadata.get("page", 0)
                }
            )

        return {"answer": str(response.content), "sources": unique_sources}

    def _build_graph(self):
        """Wire retrieve -> generate into a compiled LangGraph graph."""
        graph = StateGraph(RAGState)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("generate", self._generate)
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)
        return graph.compile()

    def invoke(self, state: dict) -> dict:
        """Run the graph for a given input state, e.g. {"question": ...}."""
        return self._graph.invoke(state)


graph = RAGPipeline()
