from django.urls import path, include
from rest_framework.routers import DefaultRouter
from SportsSyncApi.views import (
   UserViewSet,
   NewsAPIView, 
   NBAHomeView,
   PlayerListView,
   PlayerProfileView,
    TeamListView,
    TeamDetailView,
   GamesView,
   GameDetailsView,
   HistoricalMatchupsView,
   TeamsAPI,
   GamesScheduleView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
   # Include router URLs
   path('', include(router.urls)),
   
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

    # Team endpoints
    path('api/teams/', TeamListView.as_view(), name='team-list'),
    path('api/teams/<int:team_id>/', TeamDetailView.as_view(), name='team-detail'),

   # Team endpoints
   path('api/teams/', TeamsAPI.as_view(), name='teams'),
   path('api/teams/<int:team_id>/', TeamsAPI.as_view(), name='team-detail'),

   # Game endpoints
   path('api/games/', GamesView.as_view(), name='games'),
   path('api/games/schedule/', GamesScheduleView.as_view(), name='games-schedule'),
   path('api/games/<str:game_id>/details/', GameDetailsView.as_view(), name='game-details'),
]