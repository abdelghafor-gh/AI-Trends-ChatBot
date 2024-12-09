# AI Trends Chatbot

A movie information chatbot using LangChain, Pinecone, and FastAPI.

## Project Structure

```
chatbot/
├── src/                    # Source code
│   ├── api/               # API-related code
│   │   ├── models.py     # Pydantic models
│   │   └── routes.py     # FastAPI routes
│   └── core/             # Core functionality
│       ├── chat.py       # Chat and prompt flow
│       └── vector_store.py  # Pinecone operations
├── .env                   # Environment variables
├── main.py               # Application entry point
└── requirements.txt      # Project dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   CO_API_KEY=your_cohere_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

## Running the Application

Start the API server:
```bash
python main.py
```

The API will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /chat`: Send a message to the chatbot
- `GET /`: Health check endpoint

## Development

The project follows a modular structure:
- `api/`: Contains all API-related code (models, routes)
- `core/`: Contains the core chatbot functionality
  - `chat.py`: Implements the chat workflow using LangChain
  - `vector_store.py`: Handles Pinecone vector store operations
