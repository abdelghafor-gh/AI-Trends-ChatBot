# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from datetime import datetime, timedelta
from openai import AzureOpenAI
import numpy as np
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    HnswVectorSearchAlgorithmConfiguration,
    VectorSearchProfile,
    SearchField,
)

# COMMAND ----------
# Configuration
cosmos_endpoint = dbutils.secrets.get(scope="ai-feeds", key="cosmos-endpoint")
cosmos_key = dbutils.secrets.get(scope="ai-feeds", key="cosmos-key")
cosmos_database = "ai-feeds"
cosmos_collection = "news"

openai_endpoint = dbutils.secrets.get(scope="ai-feeds", key="openai-endpoint")
openai_key = dbutils.secrets.get(scope="ai-feeds", key="openai-key")
openai_deployment = "text-embedding-ada-002"

search_endpoint = dbutils.secrets.get(scope="ai-feeds", key="search-endpoint")
search_key = dbutils.secrets.get(scope="ai-feeds", key="search-key")
search_index_name = "ai-news"

# COMMAND ----------
# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    api_key=openai_key,
    api_version="2023-05-15",
    azure_endpoint=openai_endpoint
)

# Initialize Azure Search clients
search_credential = AzureKeyCredential(search_key)
index_client = SearchIndexClient(
    endpoint=search_endpoint,
    credential=search_credential
)
search_client = SearchClient(
    endpoint=search_endpoint,
    credential=search_credential,
    index_name=search_index_name
)

# COMMAND ----------
# Create or update search index
def setup_search_index():
    # Define vector search configuration
    vector_search = VectorSearch(
        algorithms=[
            HnswVectorSearchAlgorithmConfiguration(
                name="hnsw-config",
                kind="hnsw",
                parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="embedding-profile",
                algorithm="hnsw-config"
            )
        ]
    )
    
    # Define index fields
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="title", type="Edm.String"),
        SearchableField(name="description", type="Edm.String"),
        SimpleField(name="link", type="Edm.String"),
        SimpleField(name="source", type="Edm.String"),
        SimpleField(name="published_date", type="Edm.DateTimeOffset"),
        SearchField(
            name="embedding",
            type="Collection(Edm.Single)",
            vector_search_dimensions=1536,
            vector_search_profile="embedding-profile"
        )
    ]
    
    # Create index
    index = SearchIndex(
        name=search_index_name,
        fields=fields,
        vector_search=vector_search
    )
    
    try:
        index_client.create_or_update_index(index)
        print(f"Created or updated index: {search_index_name}")
    except Exception as e:
        print(f"Error creating index: {str(e)}")
        raise

# COMMAND ----------
# Read from Silver (Cosmos DB)
def read_silver_data():
    # Configure Cosmos DB connection
    cosmosConfig = {
        "spark.cosmos.accountEndpoint": cosmos_endpoint,
        "spark.cosmos.accountKey": cosmos_key,
        "spark.cosmos.database": cosmos_database,
        "spark.cosmos.container": cosmos_collection
    }
    
    # Read from Cosmos DB
    df = spark.read \
        .format("cosmos.oltp") \
        .options(**cosmosConfig) \
        .load()
    
    # Get only records from last 24 hours
    df = df.filter(
        col("processed_date") >= date_sub(current_timestamp(), 1)
    )
    
    return df

# COMMAND ----------
# Generate embeddings using Azure OpenAI
def get_embedding(text):
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=openai_deployment
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return None

# COMMAND ----------
# Transform data and generate embeddings
def transform_and_embed(df):
    # Combine title and description for embedding
    df = df.withColumn(
        "content_for_embedding",
        concat_ws(
            " ",
            col("title"),
            col("description")
        )
    )
    
    # Convert to pandas for easier processing
    pdf = df.toPandas()
    
    # Generate embeddings
    pdf["embedding"] = pdf["content_for_embedding"].apply(get_embedding)
    
    return pdf

# COMMAND ----------
# Write to Gold (Azure AI Search)
def write_to_search(df):
    # Create or update index
    setup_search_index()
    
    # Prepare documents
    documents = []
    for _, row in df.iterrows():
        if row["embedding"] is not None:
            doc = {
                "id": row["_id"],
                "title": row["title"],
                "description": row["description"],
                "link": row["link"],
                "source": row["source_name"],
                "published_date": row["published_date"].isoformat(),
                "embedding": row["embedding"]
            }
            documents.append(doc)
    
    # Upload in batches
    batch_size = 50
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        try:
            results = search_client.upload_documents(documents=batch)
            print(f"Uploaded batch {i//batch_size + 1}, success: {len([r for r in results if r.succeeded])}/{len(batch)}")
        except Exception as e:
            print(f"Error uploading batch: {str(e)}")
            raise

# COMMAND ----------
# Main execution
try:
    # Read silver data
    print("Reading silver data...")
    silver_df = read_silver_data()
    
    # Transform and generate embeddings
    print("Generating embeddings...")
    gold_df = transform_and_embed(silver_df)
    
    # Write to Azure AI Search
    print("Writing to Azure AI Search...")
    write_to_search(gold_df)
    
    print("Silver to Gold transformation completed successfully!")
    
except Exception as e:
    print(f"Error in Silver to Gold transformation: {str(e)}")
    raise
