import subprocess
import os
import json
import sys
import time

class AzureFunctionDeployer:
    def __init__(self):
        self.resource_group = "rg-ai-feeds"
        self.location = "westeurope"
        self.storage_account = "saaifeeds"  # must be globally unique
        self.function_app_name = "func-ai-feeds"  # must be globally unique
        
    def run_command(self, command, shell=True):
        """Run a command and return its output"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"Command succeeded: {command}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {command}")
            print(f"Error: {e.stderr}")
            sys.exit(1)

    def check_az_cli(self):
        """Check if Azure CLI is installed"""
        try:
            self.run_command("az --version")
            print("Azure CLI is installed")
        except:
            print("Error: Azure CLI is not installed. Please install it first.")
            print("Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
            sys.exit(1)

    def login_to_azure(self):
        """Login to Azure"""
        print("\nLogging in to Azure...")
        self.run_command("az login")

    def create_resource_group(self):
        """Create resource group"""
        print(f"\nCreating resource group: {self.resource_group}")
        self.run_command(
            f"az group create --name {self.resource_group} --location {self.location}"
        )

    def create_storage_account(self):
        """Create storage account with Data Lake Gen2"""
        print(f"\nCreating storage account: {self.storage_account}")
        self.run_command(
            f"az storage account create "
            f"--name {self.storage_account} "
            f"--resource-group {self.resource_group} "
            f"--location {self.location} "
            f"--sku Standard_LRS "
            f"--kind StorageV2 "
            f"--enable-hierarchical-namespace true"
        )

    def create_function_app(self):
        """Create Function App"""
        print(f"\nCreating function app: {self.function_app_name}")
        self.run_command(
            f"az functionapp create "
            f"--resource-group {self.resource_group} "
            f"--consumption-plan-location {self.location} "
            f"--runtime python "
            f"--runtime-version 3.9 "
            f"--functions-version 4 "
            f"--name {self.function_app_name} "
            f"--storage-account {self.storage_account} "
            f"--os-type linux"
        )

    def configure_function_app(self):
        """Configure Function App settings"""
        print("\nConfiguring function app settings...")
        self.run_command(
            f"az functionapp config appsettings set "
            f"--name {self.function_app_name} "
            f"--resource-group {self.resource_group} "
            f"--settings STORAGE_ACCOUNT_NAME={self.storage_account}"
        )

    def assign_managed_identity(self):
        """Enable and configure managed identity"""
        print("\nAssigning managed identity...")
        # Enable system-assigned managed identity
        self.run_command(
            f"az functionapp identity assign "
            f"--name {self.function_app_name} "
            f"--resource-group {self.resource_group}"
        )
        
        # Get subscription ID
        subscription_id = self.run_command(
            "az account show --query id -o tsv"
        ).strip()
        
        # Get function app's managed identity ID
        identity = self.run_command(
            f"az functionapp identity show "
            f"--name {self.function_app_name} "
            f"--resource-group {self.resource_group} "
            f"--query principalId "
            f"--output tsv"
        ).strip()
        
        # Assign Storage Blob Data Contributor role
        print("\nAssigning storage permissions...")
        self.run_command(
            f"az role assignment create "
            f"--assignee {identity} "
            f"--role 'Storage Blob Data Contributor' "
            f"--scope /subscriptions/{subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Storage/storageAccounts/{self.storage_account}"
        )

    def deploy_function(self):
        """Deploy the function code"""
        print("\nDeploying function code...")
        # Ensure we're in the function app directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        self.run_command(
            f"func azure functionapp publish {self.function_app_name}"
        )

    def deploy(self):
        """Run the full deployment process"""
        print("Starting Azure Function deployment...")
        
        self.check_az_cli()
        self.login_to_azure()
        self.create_resource_group()
        self.create_storage_account()
        self.create_function_app()
        
        # Wait for function app to be ready
        print("\nWaiting for function app to be ready...")
        time.sleep(30)
        
        self.configure_function_app()
        self.assign_managed_identity()
        self.deploy_function()
        
        print("\nDeployment completed successfully!")
        print(f"Function App URL: https://{self.function_app_name}.azurewebsites.net")

if __name__ == "__main__":
    deployer = AzureFunctionDeployer()
    deployer.deploy()
