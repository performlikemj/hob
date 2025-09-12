"""
Admin configuration for the Afrikoop backend.

This module registers the project's models with Django's admin site so
that content editors can manage mission and cleaning service pages,
events, registrations and contact messages. The list displays and
search fields are chosen to make it easy to find and edit entries.
"""
from __future__ import annotations

from django.contrib import admin
from .models import TranslatableString, EventsPageSettings, EventPlaceholder, CleaningFeature, EventImage, CleaningGalleryImage, VolunteerTier, SiteTextSettings, VolunteerGroup, VolunteerMembership

from .models import (  # noqa: F401
    CleaningServicePage,
    ContactMessage,
    Event,
    EventRegistration,
    MissionPage,
    Token,
)

# Admin site branding
admin.site.site_header = 'House of Bijou — Admin'
admin.site.site_title = 'House of Bijou Admin'
admin.site.index_title = 'Site Administration'


@admin.register(MissionPage)
class MissionPageAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'updated_at')
    search_fields = ('title_en', 'title_ja')
    fieldsets = (
        ('Text', {'fields': ('title_en', 'title_ja', 'body_en', 'body_ja')}),
        ('Hero image', {'fields': ('hero_image',)}),
    )


@admin.register(CleaningServicePage)
class CleaningServicePageAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'updated_at')
    search_fields = ('title_en', 'title_ja')
    inlines = []
    fieldsets = (
        ('Text', {'fields': ('title_en', 'title_ja', 'description_en', 'description_ja')}),
        ('Hero image', {'fields': ('image',)}),
        ('Call to action', {'fields': ('cta_en', 'cta_ja')}),
    )


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ('order', 'image', 'caption_en', 'caption_ja')
    ordering = ('order',)


@admin.register(TranslatableString)
class TranslatableStringAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'key', 'language', 'short_text', 'updated_at')
    list_filter = ('namespace', 'language')
    search_fields = ('key', 'text')
    ordering = ('namespace', 'key', 'language')

    def short_text(self, obj):  # type: ignore[no-untyped-def]
        return (obj.text[:60] + '…') if len(obj.text) > 60 else obj.text
    short_text.short_description = 'text'
    readonly_fields = ('updated_at',)
    fieldsets = (
        (None, {
            'fields': ('namespace', 'key', 'language', 'text'),
            'description': 'Manage UI copy here. Frontend loads these values at runtime and overrides defaults.'
        }),
    )


@admin.register(EventsPageSettings)
class EventsPageSettingsAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'updated_at')
    search_fields = ('title_en', 'title_ja', 'subtitle_en', 'subtitle_ja')
    inlines = []
    fieldsets = (
        ('Text', {'fields': ('title_en', 'title_ja', 'subtitle_en', 'subtitle_ja')}),
        ('Hero image', {'fields': ('hero_image',)}),
    )


class EventPlaceholderInline(admin.TabularInline):
    model = EventPlaceholder
    extra = 1
    fields = (
        'order', 'active', 'title_en', 'title_ja', 'description_en', 'description_ja', 'image',
        'cta_label_en', 'cta_label_ja', 'cta_url'
    )
    ordering = ('order',)


EventsPageSettingsAdmin.inlines.append(EventPlaceholderInline)


class CleaningFeatureInline(admin.TabularInline):
    model = CleaningFeature
    extra = 2
    fields = ('order', 'text_en', 'text_ja', 'color')
    ordering = ('order',)


CleaningServicePageAdmin.inlines.append(CleaningFeatureInline)

class CleaningGalleryInline(admin.TabularInline):
    model = CleaningGalleryImage
    extra = 3
    fields = ('order', 'image', 'caption_en', 'caption_ja')
    ordering = ('order',)

CleaningServicePageAdmin.inlines.append(CleaningGalleryInline)


@admin.register(VolunteerTier)
class VolunteerTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'active', 'member_count', 'updated_at')
    list_filter = ('active',)
    search_fields = ('name', 'description', 'members__username')
    filter_horizontal = ('members',)
    ordering = ('priority', 'name')

    def member_count(self, obj):  # type: ignore[no-untyped-def]
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(SiteTextSettings)
class SiteTextSettingsAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)
    fieldsets = (
        ('Navbar labels', {
            'fields': (
                ('home_label_en', 'home_label_ja'),
                ('events_label_en', 'events_label_ja'),
                ('cleaning_label_en', 'cleaning_label_ja'),
                ('cleaning_short_en', 'cleaning_short_ja'),
            )
        }),
        ('Auth labels', {
            'fields': (
                ('login_en', 'login_ja'),
                ('register_en', 'register_ja'),
                ('logout_en', 'logout_ja'),
            )
        }),
        ('Buttons / CTAs', {
            'fields': (
                ('browse_events_en', 'browse_events_ja'),
                ('learn_more_en', 'learn_more_ja'),
            )
        }),
        ('Social links', {
            'fields': ('instagram_url',),
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'start_datetime', 'location', 'capacity')
    search_fields = ('title_en', 'title_ja', 'location')
    list_filter = ('start_datetime',)
    inlines = [EventImageInline, EventRegistrationInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at')
    search_fields = ('event__title_en', 'user__username')
    list_filter = ('created_at',)


class VolunteerMembershipInline(admin.TabularInline):
    model = VolunteerMembership
    extra = 1
    fields = ('user', 'role', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(VolunteerGroup)
class VolunteerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'active', 'member_count', 'updated_at')
    search_fields = ('name', 'description', 'memberships__user__username')
    list_filter = ('active',)
    inlines = [VolunteerMembershipInline]
    fields = ('name', 'description', 'logo', 'active')

    def member_count(self, obj):  # type: ignore[no-untyped-def]
        return obj.memberships.count()
    member_count.short_description = 'Members'

    def logo_preview(self, obj):  # type: ignore[no-untyped-def]
        if obj.logo:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="height:28px;width:auto;border-radius:4px;"/>', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    search_fields = ('key', 'user__username')
    readonly_fields = ('key', 'user', 'created')
    list_filter = ('created',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('sent_at',)
