"""
Production settings for Azure App Service deployment.

This module extends the base settings with production-specific configuration:
- Azure PostgreSQL database (can fallback to SQLite for Free tier)
- WhiteNoise for static file serving
- Secure cookie and session settings
- CORS configuration for Azure Static Web Apps frontend
- Environment-based secrets (SECRET_KEY, DB credentials)
- Azure Blob Storage for media files (optional)

Environment variables required:
- DJANGO_SECRET_KEY: Strong random key (min 50 chars)
- DJANGO_ALLOWED_HOSTS: Comma-separated domains (e.g., "api.example.com,example.azurewebsites.net")
- AZURE_POSTGRESQL_HOST: DB host (optional, uses SQLite if not set)
- AZURE_POSTGRESQL_NAME: Database name
- AZURE_POSTGRESQL_USER: Database username
- AZURE_POSTGRESQL_PASSWORD: Database password
- FRONTEND_URL: Frontend origin for CORS (e.g., "https://example.azurestaticapps.net")
"""
from __future__ import annotations

import os
from pathlib import Path

# Import base settings
from .settings import *  # noqa: F403

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('DJANGO_SECRET_KEY environment variable must be set in production')

# Allowed hosts
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError('DJANGO_ALLOWED_HOSTS must be set (comma-separated domains)')

# Database configuration
# For Azure App Service Free tier, use SQLite on /home (persistent storage)
# For production, use Azure Database for PostgreSQL
if os.environ.get('AZURE_POSTGRESQL_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('AZURE_POSTGRESQL_NAME', 'afrikoop'),
            'USER': os.environ.get('AZURE_POSTGRESQL_USER'),
            'PASSWORD': os.environ.get('AZURE_POSTGRESQL_PASSWORD'),
            'HOST': os.environ.get('AZURE_POSTGRESQL_HOST'),
            'PORT': os.environ.get('AZURE_POSTGRESQL_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',  # Azure PostgreSQL requires SSL
            },
        }
    }
else:
    # Fallback to SQLite on Azure App Service /home (persistent across restarts)
    # Note: This is acceptable for Free tier and low traffic
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/home/site/db.sqlite3',  # Azure App Service persistent storage
        }
    }

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa: F405
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files
# Option 1: Local storage on /home (simple, works for Free tier)
MEDIA_ROOT = '/home/site/media'
MEDIA_URL = '/media/'

# Option 2: Azure Blob Storage (uncomment and configure if using Storage Account)
# if os.environ.get('AZURE_STORAGE_CONNECTION_STRING'):
#     DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
#     AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
#     AZURE_CONTAINER = 'media'

# CORS configuration
# Allow requests from Azure Static Web Apps frontend
FRONTEND_URL = os.environ.get('FRONTEND_URL', '')
if FRONTEND_URL:
    CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
    CORS_ALLOW_CREDENTIALS = True
else:
    # Fallback: allow all origins in non-production Azure environments
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Security middleware settings
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Azure App Service uses proxy
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS if ALLOWED_HOSTS else []
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in CSRF_TRUSTED_ORIGINS]

# HSTS (enable after confirming HTTPS works)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# Content type sniffing protection
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email configuration (optional, for contact form notifications)
# Configure SendGrid, Azure Communication Services, or other SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'apikey')
# EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY', '')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
# ADMINS = [('Admin', os.environ.get('ADMIN_EMAIL', 'admin@example.com'))]

# Performance optimizations
CONN_MAX_AGE = 600  # Persistent database connections (10 min)

# Jazzmin admin theme (keep existing settings)
# The Jazzmin settings from base settings.py are inherited

