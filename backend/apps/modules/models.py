from django.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from apps.blog.models import Post

User = get_user_model()


class Module(models.Model):
    """Available modules for the blog."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_installed = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default='1.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CacheEntry(models.Model):
    """Cache entries for the Cacher module."""
    
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Cache: {self.key}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class WebMention(models.Model):
    """WebMention entries for the Mentionable module."""
    
    source = models.URLField(help_text='The URL that mentions the target')
    target = models.URLField(help_text='The URL being mentioned')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='webmentions', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_url = models.URLField(blank=True)
    author_photo = models.URLField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['source', 'target']
    
    def __str__(self):
        return f"WebMention: {self.source} -> {self.target}"


class SitemapEntry(models.Model):
    """Sitemap entries for the Sitemap module."""
    
    url = models.URLField()
    last_modified = models.DateTimeField(auto_now=True)
    change_frequency = models.CharField(max_length=20, choices=[
        ('always', 'Always'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('never', 'Never'),
    ], default='weekly')
    priority = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-last_modified']
    
    def __str__(self):
        return f"Sitemap: {self.url}"


class MAPTCHAChallenge(models.Model):
    """Math-based CAPTCHA challenges."""
    
    question = models.CharField(max_length=100)
    answer = models.IntegerField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"MAPTCHA: {self.question}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class CodeHighlight(models.Model):
    """Code highlighting configurations."""
    
    language = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    file_extension = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name


class EmbedProvider(models.Model):
    """External content embed providers."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    base_url = models.URLField()
    embed_template = models.TextField(help_text='HTML template for embedding')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PostRights(models.Model):
    """Rights and attribution for posts."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='rights')
    copyright = models.CharField(max_length=200, blank=True)
    license = models.CharField(max_length=100, blank=True)
    attribution = models.TextField(blank=True)
    usage_terms = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rights for {self.post.title}"


class Theme(models.Model):
    """Blog themes."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    version = models.CharField(max_length=20, default='1.0.0')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    css_file = models.FileField(upload_to='themes/css/', blank=True, null=True)
    preview_image = models.ImageField(upload_to='themes/previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure only one theme is default
            Theme.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
