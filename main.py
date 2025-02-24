from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
import openai

app = FastAPI()

# Dummy storage for events (in a real app, this would be a database)
user_events = []

# OpenAI API Key (Replace with actual key)
OPENAI_API_KEY = "your-openai-api-key"

class EventData(BaseModel):
    user_id: str
    event_type: str
    metadata: Dict[str, str]

@app.post("/track-event")
def track_event(event: EventData):
    """Store user events"""
    user_events.append(event.dict())
    return {"message": "Event tracked successfully"}

@app.get("/get-events")
def get_events():
    """Retrieve all tracked events"""
    return {"events": user_events}

@app.post("/ask-ai")
def ask_ai(request: Request):
    """AI-enabled search to analyze user activity"""
    data = request.json()
    question = data["query"]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You analyze user data and provide insights."},
            {"role": "user", "content": question}
        ]
    )
    
    return {"response": response["choices"][0]["message"]["content"]}
