from django.urls import path
from .views import register, login, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'
urlpatterns = [
    path('register', register, name='register'),
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logintoken/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
