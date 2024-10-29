from rest_framework.views import APIView
from rest_framework.response import Response
from .games import GamesAPI
from .players import PlayersAPI
from .teams import TeamsAPI

class NBAHomeView(APIView):
    def get(self, request):
        try:
            # Get data from each API
            games_data = GamesAPI.get_games()
            player_data = PlayersAPI.get_player_of_week()
            standings_data = TeamsAPI.get_standings()
            
            response_data = {
                'games': games_data,  # This now includes live_games, upcoming_games, and recent_games
                'player_of_week': player_data,
                'standings': standings_data
            }
            
            return Response(response_data)
        except Exception as e:
            print(f"Dashboard error: {str(e)}")
            return Response({
                'games': {
                    'live_games': [],
                    'upcoming_games': [],
                    'recent_games': []
                },
                'player_of_week': None,
                'standings': {
                    'east': [],
                    'west': []
                }
            })