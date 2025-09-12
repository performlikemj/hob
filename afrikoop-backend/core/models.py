"""
Database models for the Afrikoop backend.

These models define the persistent data structures for the coop website.
They are deliberately simple and avoid any third‑party dependencies.

Language support: For user-facing content, separate fields are
provided for English and Japanese. When retrieving content for the
frontend, views can select the appropriate language based on the
``lang`` query parameter or deliver both translations.
"""
from __future__ import annotations

import secrets
import string
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class MissionPage(models.Model):
    """Model representing the mission statement of the coop.

    Only a single instance is typically used, but the model does not
    enforce this constraint so that multiple revisions can exist if
    desired. Each field suffixed with ``_en`` or ``_ja`` stores the
    translation of the content in English and Japanese respectively.
    The ``hero_image`` can be used on the homepage splash section.
    """

    title_en = models.CharField(max_length=200, blank=True)
    title_ja = models.CharField(max_length=200, blank=True)
    body_en = models.TextField(blank=True)
    body_ja = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='mission/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mission Page'
        verbose_name_plural = 'Mission Pages'

    def __str__(self) -> str:
        return self.title_en or 'Mission'


class CleaningServicePage(models.Model):
    """Model representing information about the cleaning service.

    Similar to ``MissionPage``, translations for the title and body
    text are stored in separate fields. An optional image can be
    displayed alongside the text. Only a single instance is normally
    used.
    """

    title_en = models.CharField(max_length=200, blank=True)
    title_ja = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)
    image = models.ImageField(upload_to='cleaning/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    cta_en = models.CharField(max_length=200, blank=True, default='Tell us your schedule and property details — we’ll get back with a quote.')
    cta_ja = models.CharField(max_length=200, blank=True, default='日程と物件情報をお知らせください。お見積もりをご連絡します。')

    class Meta:
        verbose_name = 'Cleaning Service Page'
        verbose_name_plural = 'Cleaning Service Pages'

    def __str__(self) -> str:
        return self.title_en or 'Cleaning Service'


class Event(models.Model):
    """Model representing an event or volunteer opportunity.

    Each event can have an optional capacity to limit the number of
    volunteers. The ``start_datetime`` field stores both date and
    time; adjust this to ``DateField`` if time is not important.
    """

    title_en = models.CharField(max_length=200)
    title_ja = models.CharField(max_length=200)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self) -> str:
        return self.title_en

    @property
    def available_slots(self) -> int | None:
        """Return the number of remaining slots or ``None`` if unlimited."""
        if self.capacity is None:
            return None
        taken = self.registrations.count()
        return max(self.capacity - taken, 0)

    def is_full(self) -> bool:
        """Return True if the event capacity has been reached."""
        return self.capacity is not None and self.registrations.count() >= self.capacity


class EventRegistration(models.Model):
    """Model representing a user's registration for an event.

    The combination of user and event is unique to prevent a user
    registering multiple times for the same event. The ``created_at``
    field records when the registration was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.event.title_en}'


class Token(models.Model):
    """Model representing an authentication token for API clients.

    This is a simple token implementation inspired by the Django REST
    Framework's token authentication. A token is a random string
    associated with a user. Clients must send the token in an
    ``Authorization: Token <key>`` header when accessing protected
    endpoints.
    """

    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def __str__(self) -> str:
        return f'Token for {self.user.username}'

    @staticmethod
    def generate_key(length: int = 40) -> str:
        """Generate a cryptographically secure random key."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @classmethod
    def create(cls, user: User) -> 'Token':
        """Create and return a new token for a user, deleting old tokens."""
        cls.objects.filter(user=user).delete()
        key = cls.generate_key()
        token = cls.objects.create(key=key, user=user)
        return token


class ContactMessage(models.Model):
    """Model representing a message sent via the contact form.

    This stores the sender's name, email and message body along with a
    timestamp. Admins can view submissions in the Django admin
    interface and respond as necessary.
    """

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self) -> str:
        return f'Message from {self.name} ({self.email})'


class TranslatableString(models.Model):
    """Key/value translations for UI strings served to the frontend.

    Each record stores a translation for a specific ``namespace`` and
    ``key`` in a given ``language``. The combination of
    ``(namespace, key, language)`` is unique. This model is intended
    for short UI strings (labels, buttons, etc.). For page content, use
    dedicated models like ``MissionPage`` with per-language fields.
    """

    LANG_CHOICES = (
        ('en', 'English'),
        ('ja', '日本語'),
    )

    namespace = models.CharField(
        max_length=50,
        default='common',
        db_index=True,
        help_text='Logical group for strings, e.g. "common", "navbar", "home".',
    )
    key = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Identifier used in the frontend, e.g. t("home") → key "home".',
    )
    language = models.CharField(
        max_length=10,
        choices=LANG_CHOICES,
        db_index=True,
        help_text='Language of this text.',
    )
    text = models.TextField(help_text='Translated text to display in the UI.')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('namespace', 'key', 'language')
        ordering = ['namespace', 'key', 'language']
        verbose_name = 'Translatable String'
        verbose_name_plural = 'Translatable Strings'

    def __str__(self) -> str:  # pragma: no cover - human readable only
        return f'[{self.language}] {self.namespace}:{self.key}'


class EventsPageSettings(models.Model):
    """Configurable content for the Events page hero.

    Provides replaceable text and imagery via Django admin so the
    frontend can display a modern hero section even when there are no
    upcoming events.
    """

    title_en = models.CharField(max_length=200, blank=True, default='Upcoming Events')
    title_ja = models.CharField(max_length=200, blank=True, default='イベント情報')
    subtitle_en = models.TextField(blank=True, default='Join community gatherings, volunteer days, and workshops. New dates drop regularly — check back soon!')
    subtitle_ja = models.TextField(blank=True, default='コミュニティイベント、ボランティア、ワークショップなど。最新情報をお見逃しなく！')
    hero_image = models.ImageField(upload_to='events/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Events Page Settings'
        verbose_name_plural = 'Events Page Settings'

    def __str__(self) -> str:
        return self.title_en or 'Events Page Settings'


class EventPlaceholder(models.Model):
    """Optional placeholder cards for the Events page when there are no events.

    These allow admins to curate sample or recurring opportunities with
    images and CTAs. Displayed when the events list is empty.
    """

    page = models.ForeignKey(EventsPageSettings, related_name='placeholders', on_delete=models.CASCADE)
    title_en = models.CharField(max_length=200)
    title_ja = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    description_ja = models.TextField(blank=True)
    image = models.ImageField(upload_to='events/placeholders/', blank=True)
    cta_label_en = models.CharField(max_length=100, blank=True)
    cta_label_ja = models.CharField(max_length=100, blank=True)
    cta_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:  # pragma: no cover
        return self.title_en


class EventImage(models.Model):
    """Optional images attached to an event for rich details."""

    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/')
    caption_en = models.CharField(max_length=200, blank=True)
    caption_ja = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:  # pragma: no cover
        return f'Image for {self.event.title_en}'


class CleaningFeature(models.Model):
    """Feature bullet for the Cleaning Service page.

    ``color`` selects the small dot color shown before each bullet on the
    frontend. It maps to the brand palette.
    """

    COLOR_CHOICES = (
        ('primary', 'Primary (Magenta/Rose)'),
        ('accent', 'Accent (Gold)'),
        ('secondary', 'Secondary (Teal)'),
    )

    page = models.ForeignKey(CleaningServicePage, related_name='features', on_delete=models.CASCADE)
    text_en = models.CharField(max_length=200)
    text_ja = models.CharField(max_length=200, blank=True)
    color = models.CharField(
        max_length=20,
        blank=True,
        choices=COLOR_CHOICES,
        help_text='Optional brand color for the bullet dot. Leave blank to use Primary.',
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:  # pragma: no cover
        return self.text_en


class CleaningGalleryImage(models.Model):
    """Gallery image for the Cleaning Service page."""

    page = models.ForeignKey(CleaningServicePage, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cleaning/gallery/')
    caption_en = models.CharField(max_length=200, blank=True)
    caption_ja = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:  # pragma: no cover
        return self.caption_en or f'Gallery image #{self.pk}'


class VolunteerTier(models.Model):
    """Simple volunteer groups/tiers that non‑technical admins can manage.

    Tiers can be used to organise members (e.g., "Core", "Hosts",
    "New Volunteers"). Users can belong to multiple tiers.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(default=0, help_text='Smaller number appears first')
    active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='volunteer_tiers', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'name']
        verbose_name = 'Volunteer Tier'
        verbose_name_plural = 'Volunteer Tiers'

    def __str__(self) -> str:  # pragma: no cover
        return self.name

    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VolunteerGroup(models.Model):
    """Logical volunteer groups (uses our own model, not auth.Group).

    Keep names simple (e.g., "Core Team", "Hosts", "New Volunteers").
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='volunteers/groups/', blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Volunteer Group'
        verbose_name_plural = 'Volunteer Groups'

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class VolunteerMembership(models.Model):
    """Membership tying users to a volunteer group with an assigned role."""

    ROLE_CHOICES = (
        ('member', 'Member'),
        ('lead', 'Lead'),
        ('coordinator', 'Coordinator'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_memberships')
    group = models.ForeignKey(VolunteerGroup, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'Volunteer Membership'
        verbose_name_plural = 'Volunteer Memberships'

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.user} @ {self.group} ({self.get_role_display()})'


class SiteTextSettings(models.Model):
    """Friendly, one‑page UI text editor for admins.

    These fields map to common UI labels used by the frontend. If a
    value is left blank the app falls back to defaults bundled in the
    frontend. Keep values short (labels/buttons).
    """

    # Navbar / basic
    home_label_en = models.CharField(max_length=50, blank=True, default='Home')
    home_label_ja = models.CharField(max_length=50, blank=True, default='ホーム')
    events_label_en = models.CharField(max_length=50, blank=True, default='Events')
    events_label_ja = models.CharField(max_length=50, blank=True, default='イベント')
    cleaning_label_en = models.CharField(max_length=50, blank=True, default='Cleaning Service')
    cleaning_label_ja = models.CharField(max_length=50, blank=True, default='清掃サービス')
    cleaning_short_en = models.CharField(max_length=50, blank=True, default='Cleaning')
    cleaning_short_ja = models.CharField(max_length=50, blank=True, default='清掃')

    # Auth
    login_en = models.CharField(max_length=50, blank=True, default='Login')
    login_ja = models.CharField(max_length=50, blank=True, default='ログイン')
    register_en = models.CharField(max_length=50, blank=True, default='Register')
    register_ja = models.CharField(max_length=50, blank=True, default='登録')
    logout_en = models.CharField(max_length=50, blank=True, default='Logout')
    logout_ja = models.CharField(max_length=50, blank=True, default='ログアウト')

    # Buttons / CTAs
    browse_events_en = models.CharField(max_length=60, blank=True, default='Browse events')
    browse_events_ja = models.CharField(max_length=60, blank=True, default='イベントを見る')
    learn_more_en = models.CharField(max_length=60, blank=True, default='Learn more')
    learn_more_ja = models.CharField(max_length=60, blank=True, default='詳しく見る')

    # Social links
    instagram_url = models.URLField(blank=True, help_text='Full URL to your Instagram profile (e.g., https://instagram.com/yourhandle)')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Text Settings'
        verbose_name_plural = 'Site Text Settings'

    def __str__(self) -> str:  # pragma: no cover
        return 'Site Text Settings'
