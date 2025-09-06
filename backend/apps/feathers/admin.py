from django.contrib import admin
from .models import (
    FeatherType, TextFeather, PhotoFeather, QuoteFeather, LinkFeather,
    VideoFeather, AudioFeather, UploaderFeather, UploadedFile
)


@admin.register(FeatherType)
class FeatherTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'created_at']


@admin.register(TextFeather)
class TextFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'format', 'created_at']
    list_filter = ['format', 'created_at']
    search_fields = ['post__title', 'content']


@admin.register(PhotoFeather)
class PhotoFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'image', 'width', 'height', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'caption']


@admin.register(QuoteFeather)
class QuoteFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'quote', 'author']


@admin.register(LinkFeather)
class LinkFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'url', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'url', 'title']


@admin.register(VideoFeather)
class VideoFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'video_file', 'video_url', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'caption']


@admin.register(AudioFeather)
class AudioFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'artist', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'title', 'artist']


@admin.register(UploaderFeather)
class UploaderFeatherAdmin(admin.ModelAdmin):
    list_display = ['post', 'file_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'description']
    
    def file_count(self, obj):
        return obj.files.count()
    file_count.short_description = 'File Count'


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'file_size_human', 'mime_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['mime_type', 'uploaded_at', 'uploaded_by']
    search_fields = ['original_name', 'uploaded_by__username']
    date_hierarchy = 'uploaded_at'
