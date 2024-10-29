from django.urls import path
from SportsSyncApi.views import (
    UserViewSet,
    NewsAPIView,
    NBAHomeView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import players, teams

class TestNBAAPI(APIView):
    def get(self, request):
        try:
            # Get teams for a basic test
            all_teams = teams.get_teams()
            leader_stats = leagueleaders.LeagueLeaders(
                season='2023-24',
                per_mode48='PerGame'
            ).get_dict()
            
            top_scorer = None
            if leader_stats['resultSet']['rowSet']:
                player = leader_stats['resultSet']['rowSet'][0]
                top_scorer = {
                    'name': player[2],
                    'team': player[3],
                    'ppg': player[22]
                }

            return Response({
                'status': 'success',
                'message': 'NBA API connection successful',
                'data': {
                    'available_endpoints': [
                        '/api/nba/home-data/',
                        '/api/nba/test/games/',
                        '/api/nba/test/players/',
                        '/api/nba/test/teams/',
                        '/api/nba/players/search/?name=<player_name>'
                    ],
                    'sample_data': {
                        'total_teams': len(all_teams),
                        'top_scorer': top_scorer
                    }
                }
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)

class TestGamesAPI(APIView):
    def get(self, request):
        try:
            board = scoreboard.ScoreBoard()
            data = board.get_dict()
            
            formatted_games = []
            for game in data.get('games', []):
                formatted_games.append({
                    'id': game['gameId'],
                    'status': game['gameStatus'],
                    'home_team': {
                        'name': game['homeTeam']['teamName'],
                        'city': game['homeTeam']['teamCity'],
                        'score': game['homeTeam'].get('score', 0),
                        'record': f"{game['homeTeam'].get('wins', 0)}-{game['homeTeam'].get('losses', 0)}"
                    },
                    'away_team': {
                        'name': game['awayTeam']['teamName'],
                        'city': game['awayTeam']['teamCity'],
                        'score': game['awayTeam'].get('score', 0),
                        'record': f"{game['awayTeam'].get('wins', 0)}-{game['awayTeam'].get('losses', 0)}"
                    },
                    'arena': game.get('arena', {}).get('arenaName'),
                    'location': game.get('arena', {}).get('arenaCity')
                })
                
            return Response({
                'status': 'success',
                'games': formatted_games
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TestPlayersAPI(APIView):
    def get(self, request):
        try:
            leaders = leagueleaders.LeagueLeaders(
                season='2023-24',
                per_mode48='PerGame'
            ).get_dict()
            
            formatted_players = []
            if leaders['resultSet']['rowSet']:
                for player in leaders['resultSet']['rowSet'][:5]:
                    formatted_players.append({
                        'name': player[2],
                        'team': player[3],
                        'stats': {
                            'games_played': player[4],
                            'minutes': player[5],
                            'points': player[22],
                            'rebounds': player[17],
                            'assists': player[18],
                            'steals': player[19],
                            'blocks': player[20]
                        }
                    })
            
            return Response({
                'status': 'success',
                'top_players': formatted_players
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TestTeamsAPI(APIView):
    def get(self, request):
        try:
            all_teams = teams.get_teams()
            # Teams data is already well formatted
            return Response({
                'status': 'success',
                'teams': all_teams
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PlayerSearchAPI(APIView):
    def get(self, request):
        name = request.query_params.get('name', '')
        if not name:
            return Response({'error': 'Name parameter is required'}, status=400)
        
        try:
            # Search for players
            found_players = players.find_players_by_full_name(name)
            
            formatted_players = []
            for player in found_players:
                formatted_players.append({
                    'id': player['id'],
                    'name': player['full_name'],
                    'is_active': player['is_active']
                })
                
            return Response({
                'status': 'success',
                'players': formatted_players
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

urlpatterns = [
    # Authentication endpoints
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    
    # News endpoint
    path('api/news/', NewsAPIView.as_view(), name='news-list'),
    
    # NBA endpoints
    path('api/nba/home-data/', NBAHomeView.as_view(), name='nba-home-data'),
    path('api/nba/test/', TestNBAAPI.as_view(), name='test-nba'),
    path('api/nba/test/games/', TestGamesAPI.as_view(), name='test-games'),
    path('api/nba/test/players/', TestPlayersAPI.as_view(), name='test-players'),
    path('api/nba/test/teams/', TestTeamsAPI.as_view(), name='test-teams'),
    path('api/nba/players/search/', PlayerSearchAPI.as_view(), name='player-search'),
]