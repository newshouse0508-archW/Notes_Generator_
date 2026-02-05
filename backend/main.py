from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
import re
from typing import Optional

app = FastAPI(
    title="StudyStream – YouTube Transcript API",
    description="Simple API to extract YouTube video transcripts",
    version="1.0.0",
)

class TranscriptRequest(BaseModel):
    url: HttpUrl

class TranscriptResponse(BaseModel):
    text: str

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    Returns None if invalid.
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",           # youtu.be / watch?v=
        r"(?:embed\/|v\/|vi\/|watch\?v=|youtu.be\/)([0-9A-Za-z_-]{11})",
        r"^([0-9A-Za-z_-]{11})$"                      # plain ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

@app.post("/transcript", response_model=TranscriptResponse)
async def get_transcript(request: TranscriptRequest):
    """
    Fetch transcript for a YouTube video.
    Tries manual subtitles first, then auto-generated.
    Returns plain text or error message.
    """
    video_id = extract_video_id(str(request.url))
    
    if not video_id:
        return TranscriptResponse(
            text="Unable to fetch transcript. Invalid YouTube URL."
        )

    try:
        # Try manual subtitles first (common languages)
        transcript_list = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['en', 'en-US', 'en-GB', 'hi']  # English + Hindi add kiya
        )
        
    except (NoTranscriptFound, TranscriptsDisabled):
        # Fallback to auto-generated
        try:
            transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_generated_transcript(['en', 'en-US', 'hi'])
            transcript_list = transcript.fetch()
        except Exception as fallback_e:
            return TranscriptResponse(
                text=f"Transcript not available. Tried manual & auto-generated. Error: {str(fallback_e)}"
            )
    
    except Exception as e:
        return TranscriptResponse(
            text=f"Unable to fetch transcript. Error: {str(e)}"
        )

    # Format to plain text
    formatter = TextFormatter()
    plain_text = formatter.format_transcript(transcript_list)
    
    return TranscriptResponse(text=plain_text.strip() or "Transcript is empty.")

# Health check / root endpoint
@app.get("/")
async def root():
    return {"message": "StudyStream Transcript API is running"}
