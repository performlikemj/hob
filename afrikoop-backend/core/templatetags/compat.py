from __future__ import annotations

from django import template

register = template.Library()


@register.filter(name="length_is")
def length_is(value, arg):  # type: ignore[no-untyped-def]
    """Compat filter for third‑party templates expecting ``length_is``.

    Returns True if ``len(value) == int(arg)``. Mirrors Django's removed
    built‑in filter so Jazzmin/Admin templates that still reference it work.
    """
    try:
        return len(value) == int(arg)
    except Exception:
        return False

