# Set environment variables for Terraform
# $env:TF_VAR_subscription_id = "your-subscription-id"
# $env:TF_VAR_client_id = "your-client-id"
# $env:TF_VAR_client_secret = "your-client-secret"
# $env:TF_VAR_tenant_id = "your-tenant-id"

# Initialize Terraform
Write-Host "`nInitializing Terraform...`n" -ForegroundColor Cyan
terraform init

# Create Terraform plan
Write-Host "`nCreating Terraform plan...`n" -ForegroundColor Cyan
terraform plan -out=tfplan

# Apply the configuration
Write-Host "`nApplying Terraform configuration...`n" -ForegroundColor Cyan
terraform apply tfplan

# Get the function app name
Write-Host "`nGetting Function App name...`n" -ForegroundColor Cyan
$FUNC_APP_NAME = terraform output -raw function_app_name

# Deploy the function code
Write-Host "`nDeploying Function code...`n" -ForegroundColor Cyan
Set-Location ..
func azure functionapp publish $FUNC_APP_NAME

Write-Host "`nDeployment completed!`n" -ForegroundColor Green
Write-Host "Function App URL: $(terraform output -raw function_app_url)" -ForegroundColor Yellow
