from django.urls import path
from . import views

urlpatterns = [
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('webmentions/', views.WebMentionListView.as_view(), name='webmention-list'),
    path('sitemap/', views.SitemapEntryListView.as_view(), name='sitemap-list'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap-xml'),
    path('code-highlights/', views.CodeHighlightListView.as_view(), name='code-highlight-list'),
    path('embed-providers/', views.EmbedProviderListView.as_view(), name='embed-provider-list'),
    path('themes/', views.ThemeListView.as_view(), name='theme-list'),
    
    # MAPTCHA
    path('maptcha/generate/', views.generate_maptcha, name='maptcha-generate'),
    path('maptcha/verify/', views.verify_maptcha, name='maptcha-verify'),
    
    # Cache
    path('cache/set/', views.cache_set, name='cache-set'),
    path('cache/get/<str:key>/', views.cache_get, name='cache-get'),
    
    # Post rights
    path('posts/<int:post_id>/rights/', views.create_post_rights, name='create-post-rights'),
]
