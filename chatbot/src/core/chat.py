"""Core chat functionality and prompt flow"""
import os
from typing import Dict
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from langchain_cohere import ChatCohere
from langgraph.graph import END, START, StateGraph
from dotenv import load_dotenv
from src.core.vector_store import get_relevant_context

# Load environment variables
load_dotenv()

# Define our state
class State(Dict):
    """State definition."""
    messages: list
    extracted_date: str = ""

def extract_date(state: State) -> State:
    """Extract date from the last message."""
    state["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return state

def generate_response(state: State) -> State:
    """Generate response with the extracted date."""
    try:
        api_key = os.getenv("CO_API_KEY")
        if not api_key:
            raise ValueError("CO_API_KEY not found in environment variables")
            
        model = ChatCohere(
            cohere_api_key=api_key,
            temperature=0
        )
        
        last_message = state["messages"][-1].content
        
        # Get relevant context from vector store
        context = get_relevant_context(last_message)
        
        # Create prompt with context
        messages = [
            ("system", "You are a knowledgeable movie expert assistant. Use the provided context to answer questions about movies accurately and helpfully."),
            ("human", f"""Here is some context about movies:
{context}

Question: {last_message}""")
        ]
        
        # Generate response with context
        ai_response = model.invoke(messages)
        response = f"As of {state['extracted_date']}, {ai_response.content}"
        
        state["messages"].append(AIMessage(content=response))
        return state
    except Exception as e:
        print(f"Error in generate_response: {str(e)}")
        raise

def create_graph():
    """Create the workflow graph."""
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("extract_date", extract_date)
    workflow.add_node("generate_response", generate_response)
    
    # Add linear edges
    workflow.add_edge(START, "extract_date")
    workflow.add_edge("extract_date", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Compile the graph
    return workflow.compile()

def process_message(message: str) -> str:
    """Process a single message through the workflow."""
    app = create_graph()
    state = {"messages": [HumanMessage(content=message)], "extracted_date": ""}
    final_state = app.invoke(state)
    return final_state["messages"][-1].content
