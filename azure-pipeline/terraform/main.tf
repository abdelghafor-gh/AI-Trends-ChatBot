terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "azurerm" {
  features {}
  # Will use your az login credentials automatically
}

# Random string for unique names
resource "random_string" "unique" {
  length  = 8
  special = false
  upper   = false
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-ai-feeds-${random_string.unique.result}"
  location = "West Europe"
}

# Storage Account with Data Lake Gen2
resource "azurerm_storage_account" "storage" {
  name                     = "saaifeeds${random_string.unique.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true # Hierarchical Namespace for Data Lake Gen2

  identity {
    type = "SystemAssigned"
  }
}

# Data Lake Gen2 File System
resource "azurerm_storage_data_lake_gen2_filesystem" "datalake" {
  name               = "ai-feeds"
  storage_account_id = azurerm_storage_account.storage.id
}

# App Service Plan for Function
resource "azurerm_service_plan" "asp" {
  name                = "asp-ai-feeds-${random_string.unique.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption plan
}

# Function App
resource "azurerm_linux_function_app" "function" {
  name                       = "func-ai-feeds-${random_string.unique.result}"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  service_plan_id            = azurerm_service_plan.asp.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    STORAGE_ACCOUNT_NAME     = azurerm_storage_account.storage.name
    FUNCTIONS_WORKER_RUNTIME = "python"
    WEBSITE_RUN_FROM_PACKAGE = "1"
    SEARCH_SERVICE_ENDPOINT  = "https://${azurerm_search_service.search.name}.search.windows.net"
    SEARCH_SERVICE_KEY       = azurerm_search_service.search.primary_key
  }
}

# Role Assignment for Function App to access Data Lake
resource "azurerm_role_assignment" "storage_role" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.function.identity[0].principal_id
}

# Cosmos DB Account
resource "azurerm_cosmosdb_account" "db" {
  name                = "cosmos-ai-feeds-${random_string.unique.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}

# Cosmos DB Database
resource "azurerm_cosmosdb_mongo_database" "mongodb" {
  name                = "ai-feeds"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.db.name
}

# Cosmos DB Collection for News
resource "azurerm_cosmosdb_mongo_collection" "news" {
  name                = "news"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.db.name
  database_name       = azurerm_cosmosdb_mongo_database.mongodb.name

  index {
    keys   = ["_id"]
    unique = true
  }

  index {
    keys = ["published_date"]
  }
}

# Data Factory
resource "azurerm_data_factory" "adf" {
  name                = "adf-ai-feeds-${random_string.unique.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  identity {
    type = "SystemAssigned"
  }
}

# Databricks Workspace
resource "azurerm_databricks_workspace" "dbw" {
  name                = "dbw-ai-feeds-${random_string.unique.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "standard"

  tags = {
    Environment = "Development"
  }
}

# Databricks Provider Configuration
provider "databricks" {
  host = azurerm_databricks_workspace.dbw.workspace_url
  azure_workspace_resource_id = azurerm_databricks_workspace.dbw.id
}

# Databricks Cluster
resource "databricks_cluster" "shared_autoscaling" {
  cluster_name            = "shared-autoscaling"
  spark_version          = "13.3.x-scala2.12"
  node_type_id           = "Standard_DS3_v2"
  autotermination_minutes = 5

  autoscale {
    min_workers = 1
    max_workers = 3
  }

  spark_conf = {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }

  custom_tags = {
    "ResourceClass" = "SingleNode"
  }
}

# Databricks Linked Service
resource "azurerm_data_factory_linked_service_azure_databricks" "databricks" {
  name            = "linked-databricks"
  data_factory_id = azurerm_data_factory.adf.id
  description     = "Databricks Linked Service"
  adb_domain      = "https://${azurerm_databricks_workspace.dbw.workspace_url}"

  existing_cluster_id = databricks_cluster.shared_autoscaling.id

  depends_on = [
    azurerm_databricks_workspace.dbw,
    databricks_cluster.shared_autoscaling
  ]
}

# Data Lake Linked Service
resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "datalake" {
  name                 = "linked-datalake"
  data_factory_id      = azurerm_data_factory.adf.id
  url                  = "https://${azurerm_storage_account.storage.name}.dfs.core.windows.net"
  use_managed_identity = true
}

# Cosmos DB Linked Service
resource "azurerm_data_factory_linked_service_cosmosdb" "cosmos" {
  name             = "linked-cosmos"
  data_factory_id  = azurerm_data_factory.adf.id
  account_endpoint = azurerm_cosmosdb_account.db.endpoint
  database         = azurerm_cosmosdb_mongo_database.mongodb.name
  account_key      = azurerm_cosmosdb_account.db.primary_key
}

# Event Grid System Topic for Function App
resource "azurerm_eventgrid_system_topic" "function_events" {
  name                   = "function-events-${random_string.unique.result}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  source_arm_resource_id = azurerm_linux_function_app.function.id
  topic_type             = "Microsoft.Web.Sites"
}

# Event Grid Trigger for Data Factory
resource "azurerm_data_factory_trigger_custom_event" "function_complete" {
  name            = "trigger-function-complete"
  data_factory_id = azurerm_data_factory.adf.id
  pipeline_name   = azurerm_data_factory_pipeline.bronze_to_gold.name

  events {
    event_type = "Microsoft.Web.FunctionExecutionSucceeded"
    scope      = azurerm_linux_function_app.function.id
  }

  annotations = ["FunctionComplete"]
}

# Azure AI Search
resource "azurerm_search_service" "search" {
  name                = "search-ai-feeds-${random_string.unique.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "free" # Free tier
  replica_count       = 1
  partition_count     = 1

  semantic_search_sku = "free" # Enable semantic search free tier
}

# Pipeline: Bronze to Gold
resource "azurerm_data_factory_pipeline" "bronze_to_gold" {
  name            = "pipeline-bronze-to-gold"
  data_factory_id = azurerm_data_factory.adf.id

  activities_json = jsonencode([
    {
      name = "Bronze to Silver",
      type = "DatabricksNotebook",
      typeProperties = {
        notebookPath = "/Shared/azure-pipeline/databricks/bronze_to_silver"
      },
      linkedServiceName = {
        referenceName = azurerm_data_factory_linked_service_azure_databricks.databricks.name,
        type          = "LinkedServiceReference"
      },
      dependsOn = []
    },
    {
      name = "Silver to Gold",
      type = "DatabricksNotebook",
      typeProperties = {
        notebookPath = "/Shared/azure-pipeline/databricks/silver_to_gold"
      },
      linkedServiceName = {
        referenceName = azurerm_data_factory_linked_service_azure_databricks.databricks.name,
        type          = "LinkedServiceReference"
      },
      dependsOn = [
        {
          activity             = "Bronze to Silver",
          dependencyConditions = ["Succeeded"]
        }
      ]
    }
  ])
}
