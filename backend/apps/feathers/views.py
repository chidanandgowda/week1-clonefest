from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    FeatherType, TextFeather, PhotoFeather, QuoteFeather, LinkFeather,
    VideoFeather, AudioFeather, UploaderFeather, UploadedFile
)
from .serializers import (
    FeatherTypeSerializer, TextFeatherSerializer, PhotoFeatherSerializer,
    QuoteFeatherSerializer, LinkFeatherSerializer, VideoFeatherSerializer,
    AudioFeatherSerializer, UploaderFeatherSerializer, FileUploadSerializer
)


class FeatherTypeListView(generics.ListAPIView):
    """List all available feather types."""
    
    queryset = FeatherType.objects.filter(is_active=True)
    serializer_class = FeatherTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TextFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle text feathers."""
    
    queryset = TextFeather.objects.all()
    serializer_class = TextFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PhotoFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle photo feathers."""
    
    queryset = PhotoFeather.objects.all()
    serializer_class = PhotoFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuoteFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle quote feathers."""
    
    queryset = QuoteFeather.objects.all()
    serializer_class = QuoteFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LinkFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle link feathers."""
    
    queryset = LinkFeather.objects.all()
    serializer_class = LinkFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VideoFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle video feathers."""
    
    queryset = VideoFeather.objects.all()
    serializer_class = VideoFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AudioFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle audio feathers."""
    
    queryset = AudioFeather.objects.all()
    serializer_class = AudioFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UploaderFeatherView(generics.RetrieveUpdateDestroyAPIView):
    """Handle uploader feathers."""
    
    queryset = UploaderFeather.objects.all()
    serializer_class = UploaderFeatherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """Upload a file for use in uploader feathers."""
    
    serializer = FileUploadSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        uploaded_file = serializer.save()
        return Response({
            'id': uploaded_file.id,
            'file': uploaded_file.file.url,
            'original_name': uploaded_file.original_name,
            'file_size': uploaded_file.file_size,
            'file_size_human': uploaded_file.file_size_human,
            'mime_type': uploaded_file.mime_type
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_text_feather(request, post_id):
    """Create a text feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = TextFeatherSerializer(data=request.data)
    if serializer.is_valid():
        text_feather = serializer.save(post=post)
        return Response(TextFeatherSerializer(text_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_photo_feather(request, post_id):
    """Create a photo feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = PhotoFeatherSerializer(data=request.data)
    if serializer.is_valid():
        photo_feather = serializer.save(post=post)
        return Response(PhotoFeatherSerializer(photo_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quote_feather(request, post_id):
    """Create a quote feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = QuoteFeatherSerializer(data=request.data)
    if serializer.is_valid():
        quote_feather = serializer.save(post=post)
        return Response(QuoteFeatherSerializer(quote_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_link_feather(request, post_id):
    """Create a link feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = LinkFeatherSerializer(data=request.data)
    if serializer.is_valid():
        link_feather = serializer.save(post=post)
        return Response(LinkFeatherSerializer(link_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_video_feather(request, post_id):
    """Create a video feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = VideoFeatherSerializer(data=request.data)
    if serializer.is_valid():
        video_feather = serializer.save(post=post)
        return Response(VideoFeatherSerializer(video_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_audio_feather(request, post_id):
    """Create an audio feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = AudioFeatherSerializer(data=request.data)
    if serializer.is_valid():
        audio_feather = serializer.save(post=post)
        return Response(AudioFeatherSerializer(audio_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_uploader_feather(request, post_id):
    """Create an uploader feather for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = UploaderFeatherSerializer(data=request.data)
    if serializer.is_valid():
        uploader_feather = serializer.save(post=post)
        return Response(UploaderFeatherSerializer(uploader_feather).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
