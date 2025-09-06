from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import (
    Module, CacheEntry, WebMention, SitemapEntry, MAPTCHAChallenge,
    CodeHighlight, EmbedProvider, PostRights, Theme
)
from .serializers import (
    ModuleSerializer, CacheEntrySerializer, WebMentionSerializer,
    SitemapEntrySerializer, MAPTCHAChallengeSerializer, CodeHighlightSerializer,
    EmbedProviderSerializer, PostRightsSerializer, ThemeSerializer
)


class ModuleListView(generics.ListAPIView):
    """List all available modules."""
    
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class WebMentionListView(generics.ListCreateAPIView):
    """List and create web mentions."""
    
    queryset = WebMention.objects.filter(is_approved=True)
    serializer_class = WebMentionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SitemapEntryListView(generics.ListAPIView):
    """List sitemap entries."""
    
    queryset = SitemapEntry.objects.filter(is_active=True)
    serializer_class = SitemapEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CodeHighlightListView(generics.ListAPIView):
    """List code highlighting languages."""
    
    queryset = CodeHighlight.objects.filter(is_active=True)
    serializer_class = CodeHighlightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmbedProviderListView(generics.ListAPIView):
    """List embed providers."""
    
    queryset = EmbedProvider.objects.filter(is_active=True)
    serializer_class = EmbedProviderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ThemeListView(generics.ListAPIView):
    """List available themes."""
    
    queryset = Theme.objects.filter(is_active=True)
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def generate_maptcha(request):
    """Generate a new MAPTCHA challenge."""
    
    import random
    import operator
    
    # Generate simple math problems
    operations = [
        ('+', operator.add),
        ('-', operator.sub),
        ('*', operator.mul),
    ]
    
    op_symbol, op_func = random.choice(operations)
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    
    if op_symbol == '-' and b > a:
        a, b = b, a
    
    question = f"{a} {op_symbol} {b} = ?"
    answer = op_func(a, b)
    
    # Create challenge
    challenge = MAPTCHAChallenge.objects.create(
        question=question,
        answer=answer,
        expires_at=timezone.now() + timezone.timedelta(minutes=10)
    )
    
    return Response({
        'id': challenge.id,
        'question': question,
        'expires_at': challenge.expires_at
    })


@api_view(['POST'])
def verify_maptcha(request):
    """Verify a MAPTCHA challenge answer."""
    
    challenge_id = request.data.get('challenge_id')
    answer = request.data.get('answer')
    
    if not challenge_id or answer is None:
        return Response({'error': 'Missing challenge_id or answer'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        challenge = MAPTCHAChallenge.objects.get(id=challenge_id)
    except MAPTCHAChallenge.DoesNotExist:
        return Response({'error': 'Invalid challenge'}, status=status.HTTP_400_BAD_REQUEST)
    
    if challenge.is_expired():
        return Response({'error': 'Challenge expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    if challenge.is_used:
        return Response({'error': 'Challenge already used'}, status=status.HTTP_400_BAD_REQUEST)
    
    if int(answer) == challenge.answer:
        challenge.is_used = True
        challenge.save()
        return Response({'success': True})
    else:
        return Response({'success': False, 'error': 'Incorrect answer'})


@api_view(['GET'])
def sitemap_xml(request):
    """Generate sitemap.xml."""
    
    entries = SitemapEntry.objects.filter(is_active=True)
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for entry in entries:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{entry.url}</loc>\n'
        xml_content += f'    <lastmod>{entry.last_modified.strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += f'    <changefreq>{entry.change_frequency}</changefreq>\n'
        xml_content += f'    <priority>{entry.priority}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type='application/xml')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cache_set(request):
    """Set a cache entry."""
    
    key = request.data.get('key')
    value = request.data.get('value')
    ttl = request.data.get('ttl', 3600)  # Default 1 hour
    
    if not key or value is None:
        return Response({'error': 'Missing key or value'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Set in Django cache
    cache.set(key, value, ttl)
    
    # Store in database for persistence
    CacheEntry.objects.update_or_create(
        key=key,
        defaults={
            'value': str(value),
            'expires_at': timezone.now() + timezone.timedelta(seconds=ttl)
        }
    )
    
    return Response({'success': True})


@api_view(['GET'])
def cache_get(request, key):
    """Get a cache entry."""
    
    # Try Django cache first
    value = cache.get(key)
    
    if value is None:
        # Try database
        try:
            entry = CacheEntry.objects.get(key=key)
            if not entry.is_expired():
                value = entry.value
                # Restore to cache
                cache.set(key, value, 3600)
            else:
                entry.delete()
        except CacheEntry.DoesNotExist:
            pass
    
    if value is not None:
        return Response({'key': key, 'value': value})
    else:
        return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_rights(request, post_id):
    """Create rights for a post."""
    
    from apps.blog.models import Post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    serializer = PostRightsSerializer(data=request.data)
    if serializer.is_valid():
        rights = serializer.save(post=post)
        return Response(PostRightsSerializer(rights).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
