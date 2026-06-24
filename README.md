# azure-appservice-devops-project
Déploiement automatisé d'une application web sur Azure App Service avec Infrastructure as Code et CI/CD.


mon-projet-devops/
│
├── .github/workflows/           <-- C'est ici que vit ton CI/CD (GitHub Actions)
│   ├── deploy-infra.yml         <-- Pipeline qui lance Terraform/Bicep
│   └── deploy-app.yml           <-- Pipeline qui build et déploie le code de ton app
│
├── iac/                         <-- Tout ton code Infrastructure as Code (IaC)
│   ├── main.tf (ou main.bicep)  <-- Fichier principal
│   ├── variables.tf             <-- Tes variables (région, tailles des instances...)
│   └── outputs.tf               <-- Les données sortantes (ex: IP publique de la VM)
│
├── ansible/                     <-- La configuration OS (Uniquement si tu utilises des VMs)
│   ├── playbook.yml             <-- Ton script de configuration (Nginx, Docker...)
│   └── inventory.ini            <-- L'adresse IP de tes cibles (souvent dynamique)
│
├── app/                         <-- Le code source de ton application web
│   ├── src/                     <-- (Code Python, Node.js, ou PHP)
│   └── Dockerfile               <-- conteneuriser  application
│
└── README.md                    <--  documentation 