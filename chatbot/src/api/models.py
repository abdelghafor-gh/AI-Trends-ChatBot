"""API models for request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="The user's message or question about movies",
        example="What are the best action movies of 2023?"
    )
    time_range: Optional[str] = Field(
        default="all",
        description="Time range for the query (e.g., 'recent', 'all', '2023')",
        example="recent"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the trending movies right now?",
                "time_range": "recent"
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(
        ...,
        description="The AI's response to the user's query",
        example="As of 2023-12-09, the top trending movies include..."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "response": "As of 2023-12-09, based on recent data, the most popular movies include 'Oppenheimer', 'Barbie', and 'The Marvels'. These films have garnered significant attention for their unique storytelling and visual effects."
            }
        }
