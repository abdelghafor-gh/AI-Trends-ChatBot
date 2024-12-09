"""API routes and endpoints"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.models import ChatRequest, ChatResponse
from src.core.chat import process_message

app = FastAPI(
    title="AI Trends Chatbot API",
    description="""
    An intelligent chatbot API that provides information about movies and trends.
    
    Features:
    - Natural language movie queries
    - Context-aware responses
    - Real-time movie information
    """,
    version="1.0.0",
    contact={
        "name": "AI Trends Chatbot Team",
        "url": "https://github.com/abdelghafor-gh/AI-Trends-ChatBot",
    },
    license_info={
        "name": "MIT",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post(
    "/chat",
    response_model=ChatResponse,
    summary="Get AI response for movie queries",
    description="""
    Send a message to the AI chatbot and receive a contextually relevant response about movies.
    The response is generated using advanced NLP and a knowledge base of movie information.
    """,
    response_description="A detailed response from the AI about the requested movie information"
)
async def chat_endpoint(request: ChatRequest):
    """
    Chat with the AI about movies:
    
    - **message**: Your question or message about movies
    - **time_range**: Optional time range for your query (default: "all")
    
    Returns a detailed response based on current movie data and trends.
    """
    try:
        response = process_message(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get(
    "/",
    summary="Check API health",
    description="Simple endpoint to check if the API is up and running",
    response_description="Returns the current health status of the API"
)
async def health_check():
    """
    Check if the API is healthy and operational.
    
    Returns:
        dict: A dictionary containing the API's health status
    """
    return {"status": "healthy"}
