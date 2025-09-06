from django.db import models
from django.contrib.auth import get_user_model
from apps.blog.models import Post

User = get_user_model()


class FeatherType(models.Model):
    """Different types of content feathers."""
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class name')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TextFeather(models.Model):
    """Text content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='text_feather')
    content = models.TextField()
    format = models.CharField(max_length=20, choices=[
        ('plain', 'Plain Text'),
        ('markdown', 'Markdown'),
        ('html', 'HTML'),
    ], default='markdown')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Text feather for {self.post.title}"


class PhotoFeather(models.Model):
    """Photo content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='photo_feather')
    image = models.ImageField(upload_to='feathers/photos/')
    caption = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Photo feather for {self.post.title}"


class QuoteFeather(models.Model):
    """Quote content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='quote_feather')
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Quote feather for {self.post.title}"


class LinkFeather(models.Model):
    """Link content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='link_feather')
    url = models.URLField()
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='feathers/links/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Link feather for {self.post.title}"


class VideoFeather(models.Model):
    """Video content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='video_feather')
    video_file = models.FileField(upload_to='feathers/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='External video URL (YouTube, Vimeo, etc.)')
    thumbnail = models.ImageField(upload_to='feathers/videos/thumbnails/', blank=True, null=True)
    caption = models.TextField(blank=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Video feather for {self.post.title}"


class AudioFeather(models.Model):
    """Audio content feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='audio_feather')
    audio_file = models.FileField(upload_to='feathers/audio/')
    title = models.CharField(max_length=200, blank=True)
    artist = models.CharField(max_length=200, blank=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Audio feather for {self.post.title}"


class UploaderFeather(models.Model):
    """File uploader feather."""
    
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='uploader_feather')
    files = models.ManyToManyField('UploadedFile', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Uploader feather for {self.post.title}"


class UploadedFile(models.Model):
    """Individual uploaded files."""
    
    file = models.FileField(upload_to='feathers/uploads/')
    original_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.original_name
    
    @property
    def file_size_human(self):
        """Return human readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
