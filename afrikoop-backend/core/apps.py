"""
Core application configuration for the Afrikoop project.

The `CoreConfig` class is automatically discovered by Django and
configures the name of the app. Additional app specific
initialisation could be added here in future.
"""
from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'