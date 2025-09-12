"""
API views for the Afrikoop backend.

These functions implement a simple JSON API without relying on third‑party
frameworks such as Django REST Framework. Each view accepts a
``django.http.HttpRequest`` and returns a ``JsonResponse``. The API is
designed for a decoupled React frontend which communicates via
HTTP. Endpoints support basic authentication using tokens and allow
users to register, log in and sign up for events.

All endpoints are exempt from CSRF protection because clients are
expected to use token authentication rather than session cookies. If
you prefer session-based authentication, remove the ``@csrf_exempt``
decorators and handle CSRF tokens on the client.
"""
from __future__ import annotations

import json
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (  # noqa: F401
    CleaningServicePage,
    ContactMessage,
    Event,
    EventRegistration,
    EventsPageSettings,
    MissionPage,
    TranslatableString,
    Token,
)

User = get_user_model()


def parse_request_body(request: HttpRequest) -> dict:
    """Parse a JSON request body and return a dict.

    If the body cannot be parsed, returns an empty dict.
    """
    try:
        body_unicode = request.body.decode('utf-8')
        if not body_unicode:
            return {}
        return json.loads(body_unicode)
    except Exception:
        return {}


def require_token(view_func):
    """Decorator to enforce token authentication on API endpoints.

    This decorator expects the ``Authorization`` header to be in the
    format ``Token <key>``. If the token is valid, ``request.user``
    will be set to the associated ``User`` instance. Otherwise a
    401 response is returned.
    """

    def wrapper(request: HttpRequest, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        prefix = 'Token '
        if not auth_header.startswith(prefix):
            return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
        key = auth_header[len(prefix):].strip()
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            return JsonResponse({'detail': 'Invalid token.'}, status=401)
        request.user = token.user  # type: ignore[attr-defined]
        return view_func(request, *args, **kwargs)

    return wrapper


@csrf_exempt
def mission_view(request: HttpRequest) -> JsonResponse:
    """Return the mission page content in JSON format.

    Query parameters:
        lang: 'en' or 'ja' to request a single language. If omitted,
              both languages are returned.

    Response body:
        {
            "title_en": "...", "title_ja": "...",
            "body_en": "...", "body_ja": "...",
            "hero_image": "/media/...jpg",
            "updated_at": "2025-09-04T12:00:00Z"
        }
    """
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    page = MissionPage.objects.first()
    lang = request.GET.get('lang')
    data: dict[str, object] = {}
    if page is None:
        # Friendly defaults so the frontend can render without admin content yet
        defaults = {
            'title_en': 'House of Bijou',
            'title_ja': 'House of Bijou',
            'body_en': 'House of Bijou celebrates the shared roots and solidarity between African/Black and Asian communities.',
            'body_ja': 'House of Bijou は、アフリカン/ブラックとアジアのコミュニティのつながりと連帯を祝福します。',
            'hero_image': None,
        }
        if lang == 'en':
            return JsonResponse({'title': defaults['title_en'], 'body': defaults['body_en'], 'hero_image': None})
        if lang == 'ja':
            return JsonResponse({'title': defaults['title_ja'], 'body': defaults['body_ja'], 'hero_image': None})
        return JsonResponse(defaults)

    if lang == 'en':
        data['title'] = page.title_en
        data['body'] = page.body_en
    elif lang == 'ja':
        data['title'] = page.title_ja
        data['body'] = page.body_ja
    else:
        data['title_en'] = page.title_en
        data['title_ja'] = page.title_ja
        data['body_en'] = page.body_en
        data['body_ja'] = page.body_ja
    data['hero_image'] = (
        request.build_absolute_uri(page.hero_image.url) if page.hero_image else None
    )
    data['updated_at'] = page.updated_at.isoformat()
    return JsonResponse(data)


@csrf_exempt
def cleaning_service_view(request: HttpRequest) -> JsonResponse:
    """Return the cleaning service page content in JSON format.

    Accepts the same ``lang`` parameter as ``mission_view``.
    """
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    page = CleaningServicePage.objects.first()
    lang = request.GET.get('lang')
    data: dict[str, object] = {}
    if page is None:
        # Return friendly defaults instead of 404 so the frontend can render placeholders
        defaults = {
            'title_en': 'Airbnb Cleaning',
            'title_ja': '清掃サービス',
            'description_en': 'Professional, reliable short-stay cleaning by members of the house. Flexible scheduling and hotel-standard turnover.',
            'description_ja': 'コミュニティメンバーによる信頼できる清掃。柔軟なスケジュールとホテル品質の仕上がり。',
            'cta_en': 'Tell us your schedule and property details — we’ll get back with a quote.',
            'cta_ja': '日程と物件情報をお知らせください。お見積もりをご連絡します。',
            'image': None,
            'features': [
                {'text_en': 'Full turnover: linens, bathroom, kitchen, reset staging', 'text_ja': 'フルターン：リネン、バスルーム、キッチン、ステージング復元', 'color': 'primary'},
                {'text_en': 'Restock consumables and basic supplies', 'text_ja': '消耗品・基本備品の補充', 'color': 'accent'},
                {'text_en': 'Flexible scheduling and quick response', 'text_ja': '柔軟なスケジュールと迅速対応', 'color': 'secondary'},
                {'text_en': 'Photo reporting on completion (optional)', 'text_ja': '写真レポート（任意）', 'color': 'primary'},
            ],
        }
        if lang == 'ja':
            return JsonResponse({
                'title': defaults['title_ja'],
                'description': defaults['description_ja'],
                'cta': defaults['cta_ja'],
                'image': None,
                'features': [{'text': f['text_ja'], 'color': f['color']} for f in defaults['features']],
            })
        elif lang == 'en':
            return JsonResponse({
                'title': defaults['title_en'],
                'description': defaults['description_en'],
                'cta': defaults['cta_en'],
                'image': None,
                'features': [{'text': f['text_en'], 'color': f['color']} for f in defaults['features']],
            })
        else:
            return JsonResponse(defaults)

    # Build features list from DB page
    features = [
        {
            'text_en': f.text_en,
            'text_ja': f.text_ja,
            'color': f.color,
        }
        for f in page.features.all()
    ]

    if lang == 'en':
        data['title'] = page.title_en
        data['description'] = page.description_en
        data['cta'] = page.cta_en
        data['features'] = [
            {'text': f['text_en'], 'color': f['color']} for f in features
        ]
    elif lang == 'ja':
        data['title'] = page.title_ja
        data['description'] = page.description_ja
        data['cta'] = page.cta_ja
        data['features'] = [
            {'text': (f['text_ja'] or f['text_en']), 'color': f['color']} for f in features
        ]
    else:
        data['title_en'] = page.title_en
        data['title_ja'] = page.title_ja
        data['description_en'] = page.description_en
        data['description_ja'] = page.description_ja
        data['cta_en'] = page.cta_en
        data['cta_ja'] = page.cta_ja
        data['features'] = features

    data['updated_at'] = page.updated_at.isoformat()
    data['image'] = (
        request.build_absolute_uri(page.image.url) if page.image else None
    )
    # Include up to 3 gallery images
    gallery = []
    for g in page.gallery_images.all()[:3]:
        gallery.append({
            'url': request.build_absolute_uri(g.image.url),
            'caption_en': g.caption_en,
            'caption_ja': g.caption_ja,
        })
    data['gallery'] = gallery
    return JsonResponse(data)


@csrf_exempt
def events_list_view(request: HttpRequest) -> JsonResponse:
    """Return a list of upcoming events.

    Query parameters:
        lang: 'en' or 'ja' to return titles/descriptions in one language.
        past: 'true' to include past events; by default only future
              events are returned.

    Response body:
        [
            {
                "id": 1,
                "title_en": "Beach Cleanup",
                "title_ja": "ビーチの清掃",
                "description_en": "...",
                "description_ja": "...",
                "start_datetime": "2025-09-20T09:00:00Z",
                "location": "Lake Biwa",
                "capacity": 10,
                "available_slots": 3
            },
            ...
        ]
    """
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    lang = request.GET.get('lang')
    include_past = request.GET.get('past', 'false').lower() == 'true'
    # Simple pagination params
    try:
        page = max(int(request.GET.get('page', '1')), 1)
    except ValueError:
        page = 1
    try:
        page_size = max(min(int(request.GET.get('page_size', '9')), 100), 1)
    except ValueError:
        page_size = 9
    now = timezone.now()
    qs = Event.objects.all()
    if not include_past:
        qs = qs.filter(start_datetime__gte=now)
    # Ensure newest first
    qs = qs.order_by('-start_datetime')

    total = qs.count()
    total_pages = (total + page_size - 1) // page_size if total else 1
    # Clamp page to available range
    if page > total_pages:
        page = total_pages

    start = (page - 1) * page_size
    end = start + page_size

    events = []
    for event in qs.select_related().prefetch_related('images')[start:end]:
        item: dict[str, object] = {
            'id': event.id,
            'start_datetime': event.start_datetime.isoformat(),
            'location': event.location,
            'capacity': event.capacity,
            'available_slots': event.available_slots,
        }
        if lang == 'en':
            item['title'] = event.title_en
            item['description'] = event.description_en
        elif lang == 'ja':
            item['title'] = event.title_ja
            item['description'] = event.description_ja
        else:
            item['title_en'] = event.title_en
            item['title_ja'] = event.title_ja
            item['description_en'] = event.description_en
            item['description_ja'] = event.description_ja
        # Attach images (no heavy resizing here)
        imgs = []
        for img in event.images.all():
            imgs.append({
                'url': request.build_absolute_uri(img.image.url),
                'caption_en': img.caption_en,
                'caption_ja': img.caption_ja,
            })
        item['images'] = imgs
        events.append(item)
    return JsonResponse({
        'results': events,
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1,
    })


@csrf_exempt
def events_page_settings_view(request: HttpRequest) -> JsonResponse:
    """Return Events page hero settings (title/subtitle/hero image).

    Accepts ``lang`` like other endpoints.
    """
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    lang = request.GET.get('lang')
    obj = EventsPageSettings.objects.first()
    if not obj:
        # Provide sensible defaults if admin has not configured it yet
        data = {
            'title_en': 'Upcoming Events',
            'title_ja': 'イベント情報',
            'subtitle_en': 'Join community gatherings, volunteer days, and workshops. New dates drop regularly — check back soon!',
            'subtitle_ja': 'コミュニティイベント、ボランティア、ワークショップなど。最新情報をお見逃しなく！',
            'hero_image': None,
        }
    else:
        data = {
            'title_en': obj.title_en,
            'title_ja': obj.title_ja,
            'subtitle_en': obj.subtitle_en,
            'subtitle_ja': obj.subtitle_ja,
            'hero_image': (
                request.build_absolute_uri(obj.hero_image.url) if obj.hero_image else None
            ),
            'updated_at': obj.updated_at.isoformat(),
        }

    if lang == 'en':
        return JsonResponse({
            'title': data.get('title_en'),
            'subtitle': data.get('subtitle_en'),
            'hero_image': data.get('hero_image'),
        })
    if lang == 'ja':
        return JsonResponse({
            'title': data.get('title_ja'),
            'subtitle': data.get('subtitle_ja'),
            'hero_image': data.get('hero_image'),
        })
    return JsonResponse(data)


@csrf_exempt
@require_token
def event_register_view(request: HttpRequest, event_id: int) -> JsonResponse:
    """Register the authenticated user for an event.

    Only ``POST`` requests are allowed. Requires the ``Authorization``
    header with a valid token. Returns 201 on success, 400 if the
    event is full or the user is already registered.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'detail': 'Event not found.'}, status=404)
    # Check if event is full
    if event.is_full():
        return JsonResponse({'detail': 'Event is full.'}, status=400)
    # Check if already registered
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'detail': 'Already registered.'}, status=400)
    # Create registration
    EventRegistration.objects.create(user=request.user, event=event)
    return JsonResponse({'detail': 'Registered successfully.'}, status=201)


@csrf_exempt
def register_user_view(request: HttpRequest) -> JsonResponse:
    """Register a new user.

    Expects a JSON payload with ``username``, ``email`` and ``password``.
    Returns 201 on success or 400 on validation errors. Passwords are
    hashed using Django's password hashing utilities.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    data = parse_request_body(request)
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not username or not email or not password:
        return JsonResponse({'detail': 'Username, email and password are required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Username already exists.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'detail': 'Email already exists.'}, status=400)
    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
    )
    token = Token.create(user)
    return JsonResponse({'token': token.key}, status=201)


@csrf_exempt
def login_view(request: HttpRequest) -> JsonResponse:
    """Log in a user and return an authentication token.

    Accepts JSON body containing ``username`` and ``password``. On
    success returns the token string. On failure returns 400 or 401.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    data = parse_request_body(request)
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return JsonResponse({'detail': 'Username and password are required.'}, status=400)
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=401)
    token = Token.create(user)
    return JsonResponse({'token': token.key})


@csrf_exempt
@require_token
def logout_view(request: HttpRequest) -> JsonResponse:
    """Invalidate the current user's token.

    Deletes the token so it can no longer be used. Clients should
    discard the token on their side as well.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    auth_header = request.headers.get('Authorization', '')
    key = auth_header.replace('Token ', '').strip()
    Token.objects.filter(key=key).delete()
    return JsonResponse({'detail': 'Logged out.'})


@csrf_exempt
def contact_view(request: HttpRequest) -> JsonResponse:
    """Process contact form submissions.

    Expects JSON with ``name``, ``email`` and ``message``. Saves the
    message in the database. Optionally send an email to site admins
    if an email backend is configured.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    data = parse_request_body(request)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    if not name or not email or not message:
        return JsonResponse({'detail': 'Name, email and message are required.'}, status=400)
    contact = ContactMessage.objects.create(name=name, email=email, message=message)
    # Optionally send an email notification here using django.core.mail.send_mail
    return JsonResponse({'detail': 'Message received. Thank you!'}, status=201)


@csrf_exempt
def i18n_view(request: HttpRequest, lang: str) -> JsonResponse:
    """Return merged UI translations for one or more namespaces.

    - Path param: ``lang`` (e.g., ``en`` or ``ja``)
    - Query param: ``ns`` comma-separated list of namespaces. Default: ``common``.

    Response: flat mapping ``{key: text}`` suitable for a single i18next namespace.
    For multiple namespaces, returns a merged dict. Later keys override earlier ones
    if duplicates exist.
    """
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    namespaces_param = request.GET.get('ns', 'common')
    namespaces = [ns.strip() for ns in namespaces_param.split(',') if ns.strip()]
    # Collect rows
    data: dict[str, str] = {}
    latest_ts: float | None = None
    for ns in namespaces:
        rows = TranslatableString.objects.filter(language=lang, namespace=ns)
        for row in rows:
            data[row.key] = row.text
            ts = row.updated_at.timestamp()
            latest_ts = max(latest_ts or ts, ts)

    # Merge in friendly site text settings (single record)
    try:
        from core.models import SiteTextSettings  # avoid circular import at module load
        st = SiteTextSettings.objects.first()
    except Exception:
        st = None
    if st:
        if lang == 'ja':
            data.update({
                'home': st.home_label_ja,
                'events': st.events_label_ja,
                'cleaning': st.cleaning_label_ja,
                'cleaning_short': st.cleaning_short_ja,
                'login': st.login_ja,
                'register': st.register_ja,
                'logout': st.logout_ja,
                'browse_events': st.browse_events_ja,
                'learn_more': st.learn_more_ja,
                'instagram_url': st.instagram_url,
            })
        else:
            data.update({
                'home': st.home_label_en,
                'events': st.events_label_en,
                'cleaning': st.cleaning_label_en,
                'cleaning_short': st.cleaning_short_en,
                'login': st.login_en,
                'register': st.register_en,
                'logout': st.logout_en,
                'browse_events': st.browse_events_en,
                'learn_more': st.learn_more_en,
                'instagram_url': st.instagram_url,
            })

    # ETag header from latest update to aid caching
    resp = JsonResponse(data)
    if latest_ts is not None:
        resp['ETag'] = f'W/"i18n-{lang}-{int(latest_ts)}"'
    return resp


@csrf_exempt
def i18n_namespace_view(request: HttpRequest, lang: str, namespace: str) -> JsonResponse:
    """Return translations for a single namespace as JSON mapping."""
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed.'}, status=405)
    rows = TranslatableString.objects.filter(language=lang, namespace=namespace)
    data = {row.key: row.text for row in rows}
    resp = JsonResponse(data)
    if rows:
        latest_ts = max(r.updated_at.timestamp() for r in rows)
        resp['ETag'] = f'W/"i18n-{lang}-{namespace}-{int(latest_ts)}"'
    return resp
