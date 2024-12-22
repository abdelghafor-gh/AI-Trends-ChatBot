# Resource Group
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

# Storage Account
output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "storage_account_id" {
  value = azurerm_storage_account.storage.id
}

# Function App
output "function_app_name" {
  value = azurerm_linux_function_app.function.name
}

output "function_app_url" {
  value = azurerm_linux_function_app.function.default_hostname
}

# Cosmos DB
output "cosmos_db_connection_string" {
  value     = azurerm_cosmosdb_account.db.connection_strings[0]
  sensitive = true
}

output "cosmos_db_endpoint" {
  value = azurerm_cosmosdb_account.db.endpoint
}

# Data Factory
output "data_factory_name" {
  value = azurerm_data_factory.adf.name
}

# Databricks
output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.dbw.workspace_url
}

output "databricks_workspace_id" {
  value = azurerm_databricks_workspace.dbw.id
}

# Event Grid
output "event_grid_topic_endpoint" {
  value = azurerm_eventgrid_system_topic.function_events.endpoint
}
