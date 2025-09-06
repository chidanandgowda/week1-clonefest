from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='post-like'),
    path('posts/<int:post_id>/stats/', views.post_stats, name='post-stats'),
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
]
