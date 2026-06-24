variable "azure_region" {
    type = string
    description = "Emplacement des ressources Azure "
    default = "francecentral"
}

variable "ressource_group_name"{
    type = string
    description = "Le Nom de ressource Groupe Azure"
    default = "rg-webapp-dev"
}

variable "admin_username"{
    type = string
    description = "Nom d'utilisateur administrateur pour la VM"
    default = "adminuser"
}



