from rest_framework import serializers
from .models import (
    Module, CacheEntry, WebMention, SitemapEntry, MAPTCHAChallenge,
    CodeHighlight, EmbedProvider, PostRights, Theme
)


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module model."""
    
    class Meta:
        model = Module
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'is_installed', 
                 'version', 'created_at', 'updated_at']


class CacheEntrySerializer(serializers.ModelSerializer):
    """Serializer for CacheEntry model."""
    
    class Meta:
        model = CacheEntry
        fields = ['id', 'key', 'value', 'expires_at', 'created_at']


class WebMentionSerializer(serializers.ModelSerializer):
    """Serializer for WebMention model."""
    
    class Meta:
        model = WebMention
        fields = ['id', 'source', 'target', 'post', 'title', 'content', 
                 'author_name', 'author_url', 'author_photo', 'is_approved', 'created_at']


class SitemapEntrySerializer(serializers.ModelSerializer):
    """Serializer for SitemapEntry model."""
    
    class Meta:
        model = SitemapEntry
        fields = ['id', 'url', 'last_modified', 'change_frequency', 'priority', 
                 'is_active', 'created_at']


class MAPTCHAChallengeSerializer(serializers.ModelSerializer):
    """Serializer for MAPTCHAChallenge model."""
    
    class Meta:
        model = MAPTCHAChallenge
        fields = ['id', 'question', 'is_used', 'created_at', 'expires_at']


class CodeHighlightSerializer(serializers.ModelSerializer):
    """Serializer for CodeHighlight model."""
    
    class Meta:
        model = CodeHighlight
        fields = ['id', 'language', 'display_name', 'file_extension', 'is_active', 'created_at']


class EmbedProviderSerializer(serializers.ModelSerializer):
    """Serializer for EmbedProvider model."""
    
    class Meta:
        model = EmbedProvider
        fields = ['id', 'name', 'slug', 'base_url', 'embed_template', 'is_active', 'created_at']


class PostRightsSerializer(serializers.ModelSerializer):
    """Serializer for PostRights model."""
    
    class Meta:
        model = PostRights
        fields = ['id', 'copyright', 'license', 'attribution', 'usage_terms', 
                 'created_at', 'updated_at']


class ThemeSerializer(serializers.ModelSerializer):
    """Serializer for Theme model."""
    
    class Meta:
        model = Theme
        fields = ['id', 'name', 'slug', 'description', 'author', 'version', 
                 'is_active', 'is_default', 'css_file', 'preview_image', 
                 'created_at', 'updated_at']
