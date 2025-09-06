from django.contrib import admin
from .models import (
    Module, CacheEntry, WebMention, SitemapEntry, MAPTCHAChallenge,
    CodeHighlight, EmbedProvider, PostRights, Theme
)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'is_installed', 'version', 'created_at']
    list_filter = ['is_active', 'is_installed', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(CacheEntry)
class CacheEntryAdmin(admin.ModelAdmin):
    list_display = ['key', 'expires_at', 'is_expired', 'created_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['key']
    date_hierarchy = 'created_at'
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True


@admin.register(WebMention)
class WebMentionAdmin(admin.ModelAdmin):
    list_display = ['source', 'target', 'author_name', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['source', 'target', 'author_name', 'title']
    date_hierarchy = 'created_at'


@admin.register(SitemapEntry)
class SitemapEntryAdmin(admin.ModelAdmin):
    list_display = ['url', 'change_frequency', 'priority', 'is_active', 'last_modified']
    list_filter = ['change_frequency', 'is_active', 'created_at']
    search_fields = ['url']
    date_hierarchy = 'created_at'


@admin.register(MAPTCHAChallenge)
class MAPTCHAChallengeAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'is_used', 'is_expired', 'created_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['question']
    date_hierarchy = 'created_at'
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True


@admin.register(CodeHighlight)
class CodeHighlightAdmin(admin.ModelAdmin):
    list_display = ['language', 'display_name', 'file_extension', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['language', 'display_name']


@admin.register(EmbedProvider)
class EmbedProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'base_url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'base_url']


@admin.register(PostRights)
class PostRightsAdmin(admin.ModelAdmin):
    list_display = ['post', 'copyright', 'license', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'copyright', 'license']


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'author', 'version', 'is_active', 'is_default', 'created_at']
    list_filter = ['is_active', 'is_default', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'author', 'description']
