from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment, Like, PostView
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer, CommentSerializer, CommentCreateSerializer,
    LikeSerializer
)


class PostListView(generics.ListCreateAPIView):
    """List and create blog posts."""
    
    queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Filter by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        
        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) | 
                Q(excerpt__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a blog post."""
    
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        instance.increment_view_count()
        
        # Track view for analytics
        if request.META.get('REMOTE_ADDR'):
            PostView.objects.create(
                post=instance,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referer=request.META.get('HTTP_REFERER', '')
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryListView(generics.ListCreateAPIView):
    """List and create categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagListView(generics.ListCreateAPIView):
    """List and create tags."""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListView(generics.ListCreateAPIView):
    """List and create comments for a post."""
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent__isnull=True).select_related('author')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(post=post)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    """Toggle like for a post."""
    
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if request.method == 'DELETE' or not created:
        like.delete()
        post.like_count = post.likes.count()
        post.save(update_fields=['like_count'])
        return Response({'liked': False})
    else:
        post.like_count = post.likes.count()
        post.save(update_fields=['like_count'])
        return Response({'liked': True})


@api_view(['GET'])
def post_stats(request, post_id):
    """Get post statistics."""
    
    post = get_object_or_404(Post, id=post_id)
    
    stats = {
        'view_count': post.view_count,
        'like_count': post.like_count,
        'comment_count': post.comment_count,
    }
    
    return Response(stats)
