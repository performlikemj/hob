"""
Django settings for the Afrikoop project.

This configuration file defines all settings required to run the
Afrikasia coop backend. It assumes a minimal installation of Django
without additional third‑party packages. The configuration uses a
SQLite database by default and serves static and media files from the
project directory during development.

Key configuration points:

* **Installed apps**: In addition to Django's default apps, the ``core``
  app is included. This app defines all project‑specific models and
  API views.
* **Middlewares**: The default Django middlewares are enabled. If you
  wish to allow cross origin requests from a separate frontend, you
  should install and configure ``django-cors-headers`` (not included
  here) and add it to the list.
* **Internationalisation**: The project uses ``en-us`` as the default
  language and ``Asia/Tokyo`` as the timezone. Although Django's
  localisation framework is enabled, translations of model fields are
  handled manually by storing separate fields for each language.
* **Media files**: User uploaded images are stored in the ``media``
  directory at the project root. Be sure to configure a proper media
  storage backend for production.

This file is designed for clarity and can be extended as needed. For
more information, see the official Django documentation:
https://docs.djangoproject.com/en/4.2/topics/settings/
"""
from __future__ import annotations

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent


def get_env(key: str, default: str | None = None) -> str:
    """Helper to read environment variables with a default fallback."""
    return os.environ.get(key, default) or ''


# SECURITY WARNING: keep the secret key used in production secret!
# It is recommended to set this via an environment variable. The default
# value here is for development only.
SECRET_KEY: str = get_env('DJANGO_SECRET_KEY', 'change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = get_env('DJANGO_DEBUG', 'True') == 'True'

# Hosts/domain names that are valid for this site; required if DEBUG is
# False. See https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS: list[str] = get_env('DJANGO_ALLOWED_HOSTS', '*').split(',')


# Application definition

INSTALLED_APPS: list[str] = [
    'jazzmin',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project apps
    'core',
]

MIDDLEWARE: list[str] = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'afrikoop.urls'

TEMPLATES: list[dict[str, object]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # Provide backwards‑compat filters (e.g., length_is) globally
            'builtins': ['core.templatetags.compat'],
        },
    },
]

WSGI_APPLICATION: str = 'afrikoop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES: dict[str, dict[str, object]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'Asia/Tokyo'

USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL: str = '/static/'
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'

MEDIA_URL: str = '/media/'
MEDIA_ROOT: Path = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# CORS settings for local development with separate frontend (Vite on 3000)
# See https://github.com/adamchainz/django-cors-headers
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
    # If you prefer to allow all in dev, uncomment the next line instead:
    # CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_HEADERS = list({
        'accept', 'accept-encoding', 'authorization', 'content-type', 'dnt', 'origin', 'user-agent', 'x-requested-with'
    })

# Jazzmin (Admin theme) settings — modern UI akin to Django Jet
JAZZMIN_SETTINGS = {
    "site_title": "House of Bijou Admin",
    "site_header": "House of Bijou",
    "site_brand": "Bijou Admin",
    "welcome_sign": "Welcome, House of Bijou team",
    "copyright": "House of Bijou",
    "site_logo": "core/logo-admin-mark.svg",
    "site_icon": "core/logo-admin-mark.svg",
    "site_logo_classes": "brand-image",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [
        "core.TranslatableString",  # keep advanced copy editor hidden from non‑dev admins
        "core.VolunteerTier",       # superseded by VolunteerGroup
    ],
    "order_with_respect_to": [
        "core.MissionPage",
        "core.CleaningServicePage",
        "core.EventsPageSettings",
        "core.Event",
        "core.EventRegistration",
        "core.VolunteerGroup",
        "core.ContactMessage",
        "core.TranslatableString",
    ],
    "icons": {
        "core.MissionPage": "fas fa-bullseye",
        "core.CleaningServicePage": "fas fa-broom",
        "core.EventsPageSettings": "fas fa-image",
        "core.Event": "fas fa-calendar-alt",
        "core.EventRegistration": "fas fa-user-check",
        "core.VolunteerGroup": "fas fa-handshake",
        "core.ContactMessage": "fas fa-envelope",
        "core.TranslatableString": "fas fa-language",
        "core.SiteTextSettings": "fas fa-font",
        "core.Token": "fas fa-key",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Guide", "url": "/admin/#guide"},
        {"name": "Site", "url": "/", "new_window": True},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # dark base, still readable
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-pink",
    "brand_small_text": False,
}
