from fastapi import FastAPI, HTTPException, status
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
    video_id = extract_video_id(str(request.url))
    
    if not video_id:
        return TranscriptResponse(
            text="Unable to fetch transcript. Invalid YouTube URL."
        )

    try:
        # सही तरीका: YouTubeTranscriptApi.get_transcript(video_id)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        formatter = TextFormatter()
        plain_text = formatter.format_transcript(transcript_list)
        
        return TranscriptResponse(text=plain_text.strip() or "Transcript is empty.")

    except TranscriptsDisabled:
        return TranscriptResponse(
            text="Transcript not available for this video. (Subtitles are disabled)"
        )
    
    except NoTranscriptFound:
        return TranscriptResponse(
            text="Transcript not available for this video."
        )
    
    except Exception as e:
        # Error को log करने के लिए print करो (Render logs में दिखेगा)
        print(f"Error fetching transcript: {str(e)}")
        return TranscriptResponse(
            text=f"Unable to fetch transcript. Error: {str(e)}"
        )

# Optional: root endpoint for testing / health check
@app.get("/")
async def root():
    return {"message": "StudyStream Transcript API is running"}
