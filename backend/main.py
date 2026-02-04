from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="StudyStream AI Backend")

class VideoRequest(BaseModel):
    youtube_url: str

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/process")
def process_video(data: VideoRequest):
    return {
        "message": "Lecture processed successfully",
        "notes": "Sample Hinglish notes generated from lecture.",
        "quiz": [
            {
                "question": "What is the main topic of the lecture?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "Option A"
            }
        ]
    }
