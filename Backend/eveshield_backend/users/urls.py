from django.urls import path
from .auth import (
    RegisterUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView
)

urlpatterns = [
    ##### Authentication API urls ######
    path('auth/register/', RegisterUserAPIView.as_view(), name='register'),
    path('auth/login/', LoginUserAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='logout'),
]
