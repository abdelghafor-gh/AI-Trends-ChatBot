from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    text: str
    sender: str  # 'user' or 'bot'
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    text: str
    sender: str = 'bot'
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseModel):
    error: str