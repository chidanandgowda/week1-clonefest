from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('me/', views.user_profile, name='user-me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
