"""Vector store operations using Azure AI Search"""
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Initialize Azure Search client
service_endpoint = "https://iat-dp-vec-ser.search.windows.net"
admin_key = "gyliiZboxtLW4MFOalWeth2LASxf5HEpuWJVNjd0FGAzSeBzigEu"
index_name = "news_chunks_embedding_extra"

credential = AzureKeyCredential(admin_key)
search_client = SearchClient(service_endpoint, index_name, credential)

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_relevant_context(query: str) -> str:
    """
    Get relevant information from Azure AI Search for a given query.
    
    Args:
        query (str): The user's question or message
        
    Returns:
        str: Formatted context from relevant entries
    """
    # Generate embedding for the query
    query_embedding = model.encode([query])[0].tolist()
    
    # Search using vector similarity
    vector_query = {
        "kind": "vector",
        "vector": query_embedding,
        "fields": "embedding",
        "k": 3,
        "exhaustive": True
    }
    
    results = search_client.search(
        search_text=query,
        # vector_queries=[vector_query],
        # select=["title", "content"]
    )
    
    # Format results into context string
    context = "\n".join([
        # f"- {doc['title']}: {doc['content']}"
        f"- {doc['title']}"
        for doc in results
    ])
    
    return context

if __name__ == "__main__":
    # Test Azure AI Search connection
    print("\n1. Testing Azure AI Search Connection...")
    try:
        results = search_client.search(search_text="*", top=1)
        list(results)  # Execute the search
        print("✅ Azure AI Search connection successful!")
    except Exception as e:
        print("❌ Azure AI Search connection failed!")
        print(f"Error: {str(e)}")

    # Test embedding model
    print("\n2. Testing Embedding Model...")
    try:
        test_text = "This is a test sentence for embedding generation"
        embedding = model.encode(test_text)
        print("✅ Embedding model working successfully!")
        print(f"Embedding shape: {embedding.shape}")
    except Exception as e:
        print("❌ Embedding generation failed!")
        print(f"Error: {str(e)}")

    # Test search functionality
    print("\n3. Testing Search Functionality...")
    try:
        test_query = "What are the latest trends in artificial intelligence?"
        context = get_relevant_context(test_query)
        print("✅ Search functionality working successfully!")
        print("\nTest Query:", test_query)
        print("\nRetrieved Context:")
        print(context)
    except Exception as e:
        print("❌ Search functionality failed!")
        print(f"Error: {str(e)}")
