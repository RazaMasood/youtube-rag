from fastapi import FastAPI, APIRouter
from modules.transcript import get_transcript_from_youtube
from model.transcript import YouTubeUrlRequest, TranscriptResponse


router = APIRouter(tags=["youtube-id-extraction"])


@router.post("/extract-id", response_model=TranscriptResponse)
def extract_youtube_id(request: YouTubeUrlRequest):
    transcript, message = get_transcript_from_youtube(request.url, request.language_code)
    return TranscriptResponse(transcript=transcript, message=message)