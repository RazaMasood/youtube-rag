from pydantic import BaseModel, Field

class YouTubeUrlRequest(BaseModel):
    url: str
    language_code: str = "en"

class TranscriptResponse(BaseModel):
    transcript: str | None
    message: str