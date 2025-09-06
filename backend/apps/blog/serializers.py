from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag, Comment, Like, PostView

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Simple user serializer for post display."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'parent', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post list view."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 'tags', 
                 'status', 'featured_image', 'view_count', 'like_count', 'comment_count',
                 'is_featured', 'created_at', 'updated_at', 'published_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post detail view."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 'category', 'tags',
                 'status', 'featured_image', 'view_count', 'like_count', 'comment_count',
                 'is_featured', 'allow_comments', 'created_at', 'updated_at', 'published_at',
                 'comments']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Post creation and updates."""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'tags', 'status',
                 'featured_image', 'is_featured', 'allow_comments']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments."""
    
    class Meta:
        model = Comment
        fields = ['content', 'parent']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model."""
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
