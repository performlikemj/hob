"""
Top level URL configuration for the Afrikoop project.

This module maps URLs to views. It delegates most of the API routing to
the ``core.urls`` module and includes Django's admin site. During
development the built-in static file serving is enabled for media
uploads. In production you should configure a proper static/media
hosting service.
"""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns: list = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)