from fastapi import APIRouter, HTTPException, Depends
from ..models import ChatRequest, ChatResponse, ErrorResponse
from ..config import get_settings
import cohere

router = APIRouter()
settings = get_settings()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Initialize Cohere client
        co = cohere.Client(settings.COHERE_API_KEY)
        
        # Create chat completion using Cohere
        response = co.chat(
            message=request.message,
            model="command",  # Cohere's recommended model for chat
            temperature=0.7,
            preamble="""You are an AI expert who specializes in discussing AI trends, developments, and technologies. 
            Provide informative and accurate responses about artificial intelligence topics.""",
        )
        
        # Extract the response text
        response_text = response.text
        
        return ChatResponse(text=response_text)
    except cohere.CohereError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))