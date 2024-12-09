"""Vector store operations using Pinecone"""
import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone

# Load environment variables
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("sample-movies")

def get_relevant_context(query: str) -> str:
    """
    Get relevant movie information from Pinecone for a given query.
    
    Args:
        query (str): The user's question or message
        
    Returns:
        str: Formatted context from relevant movie entries
    """
    # Convert query to vector embedding
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    
    # Search Pinecone index
    results = index.query(
        vector=query_embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )
    
    # Format results into context string
    context = "\n".join([
        f"- {result.metadata.get('title', 'Unknown')}: {result.metadata.get('description', 'No description')}"
        for result in results.matches
    ])
    
    return context
