from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import configure_logging
from app.api.schemas import ChatRequest, ChatResponse
from app.api.chat_service import ChatService


class ChatAPI:
    """Builds and configures the FastAPI app for the CV chat endpoint."""

    ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

    def __init__(self) -> None:
        self._service = ChatService()
        self.app = FastAPI(title="CV Screener Chat API")
        self._configure_cors()
        self._register_routes()

    def _configure_cors(self) -> None:
        """Allow the local React dev server to call this API."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.ALLOWED_ORIGINS,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self) -> None:
        """Wire up the health and chat endpoints."""

        @self.app.get("/api/health")
        def health() -> dict:
            return {"status": "ok"}

        @self.app.post("/api/chat", response_model=ChatResponse)
        def chat(request: ChatRequest) -> ChatResponse:
            result = self._service.ask(request.question)
            return ChatResponse(answer=result["answer"], sources=result.get("sources", []))


configure_logging()
api = ChatAPI()
app = api.app


def main() -> None:
    """Entry point: run the API with uvicorn."""
    import uvicorn

    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
