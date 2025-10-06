// Main Bicep template for Afrikoop Azure deployment
// Deploys: App Service (Django backend), Static Web App (React frontend)
// Optional: PostgreSQL Flexible Server (uncomment if using managed DB)

@description('Environment name (e.g., dev, staging, prod)')
param environment string = 'prod'

@description('Location for backend resources (App Service)')
param location string = 'japaneast'

@description('Location for frontend (Static Web Apps)')
param frontendLocation string = 'eastasia'

@description('Django secret key (min 50 characters)')
@secure()
param djangoSecretKey string

@description('Admin email for Django superuser')
param adminEmail string = 'admin@example.com'

@description('Admin password for Django superuser')
@secure()
param adminPassword string

@description('Backend custom domain (optional)')
param backendCustomDomain string = ''

@description('Frontend custom domain (optional)')
param frontendCustomDomain string = ''

@description('Enable PostgreSQL database (false uses SQLite)')
param enablePostgreSQL bool = false

@description('PostgreSQL admin username')
param postgresAdminUsername string = 'afrikoop_admin'

@description('PostgreSQL admin password')
@secure()
param postgresAdminPassword string = ''

// Variables
var appServicePlanName = 'asp-afrikoop-${environment}'
var appServiceName = 'app-afrikoop-backend-${environment}'
var staticWebAppName = 'swa-afrikoop-frontend-${environment}'
var postgresServerName = 'psql-afrikoop-${environment}-${uniqueString(resourceGroup().id)}'
var postgresDatabaseName = 'afrikoop'

// App Service Plan (Free or Basic tier)
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'F1'  // Free tier (60 CPU min/day). Use 'B1' for Basic ($13/mo) if needed
    tier: 'Free'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true  // Required for Linux
  }
}

// App Service (Django backend)
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: appServiceName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: false  // Free tier doesn't support Always On
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      pythonVersion: '3.11'
      appCommandLine: 'bash startup.sh'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'DJANGO_SETTINGS_MODULE'
          value: 'afrikoop.settings_prod'
        }
        {
          name: 'DJANGO_SECRET_KEY'
          value: djangoSecretKey
        }
        {
          name: 'DJANGO_ALLOWED_HOSTS'
          value: '${appServiceName}.azurewebsites.net${backendCustomDomain != '' ? ',${backendCustomDomain}' : ''}'
        }
        {
          name: 'FRONTEND_URL'
          value: frontendCustomDomain != '' ? 'https://${frontendCustomDomain}' : 'https://${staticWebAppName}.azurestaticapps.net'
        }
        {
          name: 'PYTHONUNBUFFERED'
          value: '1'
        }
        {
          name: 'ADMIN_EMAIL'
          value: adminEmail
        }
        {
          name: 'ADMIN_PASSWORD'
          value: adminPassword
        }
      ]
    }
  }
}

// PostgreSQL Flexible Server (optional, for production)
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = if (enablePostgreSQL) {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B1ms'  // Smallest burstable tier ($25-45/mo)
    tier: 'Burstable'
  }
  properties: {
    version: '15'
    administratorLogin: postgresAdminUsername
    administratorLoginPassword: postgresAdminPassword
    storage: {
      storageSizeGB: 32  // Minimum for Flexible Server
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

// PostgreSQL Database
resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-03-01-preview' = if (enablePostgreSQL) {
  parent: postgresServer
  name: postgresDatabaseName
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// PostgreSQL Firewall Rule (allow Azure services)
resource postgresFirewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = if (enablePostgreSQL) {
  parent: postgresServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Update App Service with PostgreSQL connection string
resource appServiceConnectionString 'Microsoft.Web/sites/config@2023-01-01' = if (enablePostgreSQL) {
  parent: appService
  name: 'appsettings'
  properties: {
    AZURE_POSTGRESQL_HOST: postgresServer.properties.fullyQualifiedDomainName
    AZURE_POSTGRESQL_NAME: postgresDatabaseName
    AZURE_POSTGRESQL_USER: postgresAdminUsername
    AZURE_POSTGRESQL_PASSWORD: postgresAdminPassword
    AZURE_POSTGRESQL_PORT: '5432'
  }
}

// Static Web App (React frontend)
resource staticWebApp 'Microsoft.Web/staticSites@2023-01-01' = {
  name: staticWebAppName
  location: frontendLocation
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    repositoryUrl: ''  // Set via GitHub Actions
    branch: ''  // Set via GitHub Actions
    buildProperties: {
      appLocation: 'afrikoop-frontend'
      apiLocation: ''
      outputLocation: 'dist'
    }
  }
}

// Static Web App custom domain (optional)
resource staticWebAppCustomDomain 'Microsoft.Web/staticSites/customDomains@2023-01-01' = if (frontendCustomDomain != '') {
  parent: staticWebApp
  name: frontendCustomDomain
  properties: {}
}

// Outputs
output appServiceHostname string = appService.properties.defaultHostName
output staticWebAppUrl string = 'https://${staticWebApp.properties.defaultHostname}'
output staticWebAppDeploymentToken string = staticWebApp.listSecrets().properties.apiKey
output postgresHost string = enablePostgreSQL ? postgresServer.properties.fullyQualifiedDomainName : ''

