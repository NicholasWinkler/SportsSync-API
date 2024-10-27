from django.contrib import admin
from django.urls import path
from SportsSyncApi.views import UserViewSet
from SportsSyncApi.views import NewsAPIView

urlpatterns = [
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('api/news/', NewsAPIView.as_view(), name='news-list'),
]
