from pydantic import BaseModel

class RagRequest(BaseModel):
    transcript: str
    question: str

class RagResponse(BaseModel):
    answer: str | None
    error: str | None = None