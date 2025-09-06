from rest_framework import serializers
from .models import (
    FeatherType, TextFeather, PhotoFeather, QuoteFeather, LinkFeather,
    VideoFeather, AudioFeather, UploaderFeather, UploadedFile
)


class FeatherTypeSerializer(serializers.ModelSerializer):
    """Serializer for FeatherType model."""
    
    class Meta:
        model = FeatherType
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'created_at']


class UploadedFileSerializer(serializers.ModelSerializer):
    """Serializer for UploadedFile model."""
    
    file_size_human = serializers.ReadOnlyField()
    
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'original_name', 'file_size', 'file_size_human', 
                 'mime_type', 'uploaded_at']


class TextFeatherSerializer(serializers.ModelSerializer):
    """Serializer for TextFeather model."""
    
    class Meta:
        model = TextFeather
        fields = ['id', 'content', 'format', 'created_at', 'updated_at']


class PhotoFeatherSerializer(serializers.ModelSerializer):
    """Serializer for PhotoFeather model."""
    
    class Meta:
        model = PhotoFeather
        fields = ['id', 'image', 'caption', 'alt_text', 'width', 'height', 
                 'created_at', 'updated_at']


class QuoteFeatherSerializer(serializers.ModelSerializer):
    """Serializer for QuoteFeather model."""
    
    class Meta:
        model = QuoteFeather
        fields = ['id', 'quote', 'author', 'source', 'created_at', 'updated_at']


class LinkFeatherSerializer(serializers.ModelSerializer):
    """Serializer for LinkFeather model."""
    
    class Meta:
        model = LinkFeather
        fields = ['id', 'url', 'title', 'description', 'thumbnail', 
                 'created_at', 'updated_at']


class VideoFeatherSerializer(serializers.ModelSerializer):
    """Serializer for VideoFeather model."""
    
    class Meta:
        model = VideoFeather
        fields = ['id', 'video_file', 'video_url', 'thumbnail', 'caption', 
                 'duration', 'created_at', 'updated_at']


class AudioFeatherSerializer(serializers.ModelSerializer):
    """Serializer for AudioFeather model."""
    
    class Meta:
        model = AudioFeather
        fields = ['id', 'audio_file', 'title', 'artist', 'duration', 
                 'created_at', 'updated_at']


class UploaderFeatherSerializer(serializers.ModelSerializer):
    """Serializer for UploaderFeather model."""
    
    files = UploadedFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = UploaderFeather
        fields = ['id', 'files', 'description', 'created_at', 'updated_at']


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for file uploads."""
    
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def create(self, validated_data):
        file = validated_data['file']
        validated_data.update({
            'original_name': file.name,
            'file_size': file.size,
            'mime_type': file.content_type,
            'uploaded_by': self.context['request'].user
        })
        return super().create(validated_data)
