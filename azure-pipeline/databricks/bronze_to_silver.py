# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from datetime import datetime, timedelta

# COMMAND ----------
# Configuration
storage_account = dbutils.secrets.get(scope="ai-feeds", key="storage-account-name")
cosmos_endpoint = dbutils.secrets.get(scope="ai-feeds", key="cosmos-endpoint")
cosmos_key = dbutils.secrets.get(scope="ai-feeds", key="cosmos-key")
cosmos_database = "ai-feeds"
cosmos_collection = "news"

# COMMAND ----------
# Read from Bronze (Data Lake)
def read_bronze_data():
    # Get today's date for the path
    today = datetime.now()
    bronze_path = f"abfss://ai-feeds@{storage_account}.dfs.core.windows.net/raw/year={today.year}/month={today.strftime('%m')}/day={today.strftime('%d')}"
    
    # Read JSON files
    bronze_df = spark.read.json(bronze_path)
    return bronze_df.select("entries.*")

# COMMAND ----------
# Transform data
def transform_data(df):
    # Explode the entries array
    df_processed = df.select(
        col("source_category"),
        col("source_name"),
        col("source_url"),
        col("title"),
        col("link"),
        col("description"),
        to_timestamp(col("published_date")).alias("published_date"),
        col("author"),
        explode_outer(col("tags")).alias("tag")
    )
    
    # Group tags
    df_processed = df_processed.groupBy(
        "source_category", "source_name", "source_url", "title", 
        "link", "description", "published_date", "author"
    ).agg(collect_list("tag").alias("tags"))
    
    # Add processing metadata
    df_processed = df_processed.withColumn("processed_date", current_timestamp())
    df_processed = df_processed.withColumn("_id", sha2(concat_ws("_", col("source_name"), col("title")), 256))
    
    return df_processed

# COMMAND ----------
# Write to Silver (Cosmos DB)
def write_to_cosmos(df):
    # Configure Cosmos DB connection
    cosmosConfig = {
        "spark.cosmos.accountEndpoint": cosmos_endpoint,
        "spark.cosmos.accountKey": cosmos_key,
        "spark.cosmos.database": cosmos_database,
        "spark.cosmos.container": cosmos_collection,
        "spark.cosmos.write.strategy": "ItemOverwrite"
    }
    
    # Write to Cosmos DB
    df.write \
        .format("cosmos.oltp") \
        .options(**cosmosConfig) \
        .mode("append") \
        .save()

# COMMAND ----------
# Main execution
try:
    # Read bronze data
    print("Reading bronze data...")
    bronze_df = read_bronze_data()
    
    # Transform data
    print("Transforming data...")
    silver_df = transform_data(bronze_df)
    
    # Write to Cosmos DB
    print("Writing to Cosmos DB...")
    write_to_cosmos(silver_df)
    
    print("Bronze to Silver transformation completed successfully!")
    
except Exception as e:
    print(f"Error in Bronze to Silver transformation: {str(e)}")
    raise
