from django.urls import path
from SportsSyncApi.views import (
    UserViewSet,
    NewsAPIView,
    NBAHomeView,
    PlayerListView,
    PlayerProfileView,
)

urlpatterns = [
    # Authentication endpoints
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),

    # News endpoint
    path('api/news/', NewsAPIView.as_view(), name='news-list'),

    # NBA endpoint
    path('api/nba/home-data/', NBAHomeView.as_view(), name='nba-home-data'),

    # Player endpoints
    path('api/players/', PlayerListView.as_view(), name='player-list'),
    path('api/players/<int:player_id>/', PlayerProfileView.as_view(), name='player-detail'),
]
