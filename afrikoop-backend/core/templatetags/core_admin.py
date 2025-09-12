from __future__ import annotations

from datetime import timedelta

from django import template
from django.utils import timezone

from core.models import ContactMessage, Event, EventRegistration

register = template.Library()


@register.simple_tag
def total_events() -> int:
    return Event.objects.count()


@register.simple_tag
def upcoming_events_count() -> int:
    return Event.objects.filter(start_datetime__gte=timezone.now()).count()


@register.simple_tag
def registrations_count() -> int:
    return EventRegistration.objects.count()


@register.simple_tag
def contact_count(days: int = 30) -> int:
    since = timezone.now() - timedelta(days=days)
    return ContactMessage.objects.filter(sent_at__gte=since).count()


@register.simple_tag
def upcoming_events(limit: int = 5):
    return (
        Event.objects.filter(start_datetime__gte=timezone.now())
        .order_by('start_datetime')[:limit]
    )


@register.simple_tag
def recent_messages(limit: int = 5):
    return ContactMessage.objects.order_by('-sent_at')[:limit]

