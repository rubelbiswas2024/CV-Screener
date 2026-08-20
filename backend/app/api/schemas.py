from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class Source(BaseModel):
    candidate_id: str = ""
    candidate_name: str = ""
    file: str = ""
    page: int = 0

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []
