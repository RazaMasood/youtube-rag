from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
import re
from typing import Optional, Tuple

def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the YouTube video ID from different formats of URLs.
    """
    patterns = [
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com.*(?:v=|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(video_id: str) -> Tuple[str, list]:
    """
    Gets available transcript languages for a video.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = []
        for transcript in transcript_list:
            languages.append({
                'code': transcript.language_code,
                'name': transcript.language,
                'is_generated': transcript.is_generated
            })
        return "success", languages
    except Exception as e:
        return str(e), []

def get_transcript_from_youtube(url: str, language_code: str = "en") -> Tuple[Optional[str], str]:
    """
    Attempts to fetch a transcript from a YouTube video in the specified language.
    Returns (transcript_text, status_message)
    """
    video_id = extract_video_id(url)
    if not video_id:
        return None, "Invalid URL format or missing video ID."

    try:
        # Try to get transcript in specified language
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript_text = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript_text, f"Transcript successfully extracted in {language_code}!"
        
    except NoTranscriptFound:
        # Try to get any available transcript
        try:
            transcript_info = YouTubeTranscriptApi.list_transcripts(video_id)
            available_transcripts = list(transcript_info)
            if available_transcripts:
                transcript = available_transcripts[0]
                transcript_data = transcript.fetch()
                transcript_text = " ".join(chunk["text"] for chunk in transcript_data)
                return transcript_text, f"Transcript extracted in {transcript.language} (fallback)"
            else:
                return None, "No transcripts available for this video."
        except Exception as e:
            return None, f"Error accessing transcripts: {str(e)}"
            
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except VideoUnavailable:
        return None, "Video is unavailable or private."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"