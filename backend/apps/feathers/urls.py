from django.urls import path
from . import views

urlpatterns = [
    path('types/', views.FeatherTypeListView.as_view(), name='feather-type-list'),
    path('upload/', views.upload_file, name='file-upload'),
    
    # Text feathers
    path('text/<int:pk>/', views.TextFeatherView.as_view(), name='text-feather-detail'),
    path('posts/<int:post_id>/text/', views.create_text_feather, name='create-text-feather'),
    
    # Photo feathers
    path('photo/<int:pk>/', views.PhotoFeatherView.as_view(), name='photo-feather-detail'),
    path('posts/<int:post_id>/photo/', views.create_photo_feather, name='create-photo-feather'),
    
    # Quote feathers
    path('quote/<int:pk>/', views.QuoteFeatherView.as_view(), name='quote-feather-detail'),
    path('posts/<int:post_id>/quote/', views.create_quote_feather, name='create-quote-feather'),
    
    # Link feathers
    path('link/<int:pk>/', views.LinkFeatherView.as_view(), name='link-feather-detail'),
    path('posts/<int:post_id>/link/', views.create_link_feather, name='create-link-feather'),
    
    # Video feathers
    path('video/<int:pk>/', views.VideoFeatherView.as_view(), name='video-feather-detail'),
    path('posts/<int:post_id>/video/', views.create_video_feather, name='create-video-feather'),
    
    # Audio feathers
    path('audio/<int:pk>/', views.AudioFeatherView.as_view(), name='audio-feather-detail'),
    path('posts/<int:post_id>/audio/', views.create_audio_feather, name='create-audio-feather'),
    
    # Uploader feathers
    path('uploader/<int:pk>/', views.UploaderFeatherView.as_view(), name='uploader-feather-detail'),
    path('posts/<int:post_id>/uploader/', views.create_uploader_feather, name='create-uploader-feather'),
]
