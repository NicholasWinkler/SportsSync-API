# SportsSyncApi/views/home.py

from django.http import JsonResponse
from django.views import View
from nba_api.stats.endpoints import leaguegamefinder, leagueleaders

class HomePageData(View):
    def get(self, request):
        try:
            # Fetching featured games
            game_finder = leaguegamefinder.LeagueGameFinder()
            games = game_finder.get_data_frames()[0]  # Get the first DataFrame
            featured_games = games[['GAME_ID', 'GAME_DATE', 'TEAM_NAME', 'HOME_TEAM', 'VISITOR_TEAM']].head(5).to_dict(orient='records')

            # Fetching league leaders (top players)
            league_leaders = leagueleaders.LeagueLeaders()
            leaders_data = league_leaders.get_data_frames()[0]  # Get the first DataFrame
            top_player = leaders_data[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS']].iloc[0].to_dict()
            player_of_week = {
                "name": top_player['PLAYER_NAME'],
                "team": top_player['TEAM_ABBREVIATION'],
                "points": top_player['PTS'],
            }

            # Fetching current standings
            current_standings = league_leaders.get_data_frames()[0]  # Here you can modify as needed
            standings_data = current_standings[['TEAM_NAME', 'W', 'L']].to_dict(orient='records')

            # Combine all data
            response_data = {
                "featured_games": featured_games,
                "player_of_week": player_of_week,
                "current_standings": standings_data,
            }
            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
