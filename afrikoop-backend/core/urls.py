"""
URL configuration for the core app.

This module declares the API endpoints used by the frontend. Each
endpoint maps to a view function defined in ``core.views``. All
routes return JSON responses and are prefixed with ``/api/`` in the
project's root ``urls.py``.
"""
from __future__ import annotations

from django.urls import path

from . import views


urlpatterns = [
    # Public content endpoints
    path('mission/', views.mission_view, name='mission'),
    path('cleaning-service/', views.cleaning_service_view, name='cleaning-service'),
    path('events/', views.events_list_view, name='events-list'),
    path('events-page/', views.events_page_settings_view, name='events-page'),
    # Event registration
    path('events/<int:event_id>/register/', views.event_register_view, name='event-register'),
    # Authentication endpoints
    path('auth/register/', views.register_user_view, name='register-user'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    # Contact form
    path('contact/', views.contact_view, name='contact'),
    # i18n bundles for the frontend
    path('i18n/<str:lang>/', views.i18n_view, name='i18n-merged'),
    path('i18n/<str:lang>/<str:namespace>.json', views.i18n_namespace_view, name='i18n-namespace'),
]
