"""Main entry point for the chatbot API"""
import uvicorn
from src.api.routes import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9000, reload=True)
