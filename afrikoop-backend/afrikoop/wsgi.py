"""
WSGI config for Afrikoop project.

It exposes the WSGI callable as a module‑level variable named ``application``.
See https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/ for more details.
"""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afrikoop.settings')

application = get_wsgi_application()