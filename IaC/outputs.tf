output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "Name of the Azure resource group created by main.tf."
}

output "app_service_plan_name" {
  value       = azurerm_app_service_plan.asp.name
  description = "Name of the Azure App Service plan created by main.tf."
}

output "app_service_name" {
  value       = azurerm_app_service.app.name
  description = "Name of the Azure App Service created by main.tf."
}

output "app_service_default_hostname" {
  value       = azurerm_app_service.app.default_site_hostname
  description = "Default hostname of the deployed Azure App Service."
}

output "app_service_url" {
  value       = "https://${azurerm_app_service.app.default_site_hostname}"
  description = "URL of the deployed Azure App Service."
}
