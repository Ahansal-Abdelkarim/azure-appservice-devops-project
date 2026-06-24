resource "azurerm_resource_group" "rg" {
  name    = var.ressource_group_name
  location = var.azure_region
}