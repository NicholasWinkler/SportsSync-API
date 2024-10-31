# games.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv2
from datetime import datetime


class GamesAPI:
    @staticmethod
    def get_games():
        """Fetches live, upcoming, and recent games."""
        try:
            live_games, upcoming_games, recent_games = [], [], []
            board = scoreboard.ScoreBoard()
            data = board.get_dict()
            
            if 'scoreboard' in data and 'games' in data['scoreboard']:
                games = data['scoreboard']['games']
                print(f"Found {len(games)} games")
                
                for game in games:
                    game_data = GamesAPI._format_game_data(game)
                    
                    if game['period'] > 0 and game['gameStatus'] != 3:
                        live_games.append(game_data)
                    elif game['gameStatus'] == 3:
                        recent_games.append(game_data)
                    else:
                        upcoming_games.append(game_data)

            return {'live_games': live_games, 'upcoming_games': upcoming_games, 'recent_games': recent_games}
            
        except Exception as e:
            print(f"Error in get_games: {str(e)}")
            return {'live_games': [], 'upcoming_games': [], 'recent_games': []}

    @staticmethod
    def get_game_details(game_id):
        """Fetches detailed information for a specific game by game ID."""
        try:
            board = scoreboard.ScoreBoard()
            games = board.get_dict()['scoreboard']['games']
            game_basic = next((g for g in games if g['gameId'] == game_id), None)

            if not game_basic:
                return None

            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            box_score_data = box_score.get_dict()

            return {
                'basic_info': GamesAPI._format_game_data(game_basic),
                'box_score': {
                    'home_team_stats': box_score_data.get('HomeTeamStats', []),
                    'away_team_stats': box_score_data.get('AwayTeamStats', []),
                    'player_stats': box_score_data.get('PlayerStats', [])
                }
            }
        except Exception as e:
            print(f"Error getting game details: {str(e)}")
            return None

    @staticmethod
    def _format_game_data(game):
        """Formats game data for consistent response structure."""
        return {
            'id': game['gameId'],
            'status': game['gameStatusText'],
            'date': game['gameEt'],
            'time': game['gameStatusText'],
            'home_team': {
                'id': game['homeTeam']['teamId'],
                'full_name': f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}",
                'record': f"{game['homeTeam']['wins']}-{game['homeTeam']['losses']}",
                'score': game['homeTeam'].get('score', 0)
            },
            'visitor_team': {
                'id': game['awayTeam']['teamId'],
                'full_name': f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}",
                'record': f"{game['awayTeam']['wins']}-{game['awayTeam']['losses']}",
                'score': game['awayTeam'].get('score', 0)
            }
        }

# class GameDetailsAPI:
    API_KEY = "b81b0bea-7ecc-4760-a3f7-d2a42e0413b4"  # Your Ball Don't Lie API key
    BASE_URL = "https://api.balldontlie.io/v1"
    TIMEOUT = (5, 10)  # (connect timeout, read timeout)

    @staticmethod
    def get_all_games(per_page=25, cursor=None, start_date=None, end_date=None):
        """Fetches all games with optional filtering."""
        if start_date is None and end_date is None:
            today = datetime.now().date().isoformat()  # Get today's date
            start_date = today
            end_date = today

        params = {
            'per_page': per_page,
            'cursor': cursor,
            'start_date': start_date,
            'end_date': end_date
        }

        # Filter out any None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(f"{GameDetailsAPI.BASE_URL}/games", params=params, timeout=GameDetailsAPI.TIMEOUT)
            response.raise_for_status()  # Raise an error for bad responses
            
            games_data = response.json()
            return games_data  # Return the JSON response directly
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching games: {str(e)}")
            return None

    @staticmethod
    def get_game_by_id(game_id):
        """Fetches a specific game by its ID."""
        try:
            response = requests.get(f"{GameDetailsAPI.BASE_URL}/games/{game_id}", timeout=GameDetailsAPI.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching game {game_id}: {str(e)}")
            return None

class GameDetailsView(APIView):
    def get(self, request):
        """Handles GET requests to retrieve game details."""
        game_id = request.query_params.get('game_id', None)  # Check if a specific game ID is requested
        if game_id:
            game = GameDetailsAPI.get_game_by_id(game_id)
            if game:
                return Response(game, status=status.HTTP_200_OK)
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        # Remove per_page and cursor for today’s games only
        games = GameDetailsAPI.get_all_games()

        if games is not None:
            return Response(games, status=status.HTTP_200_OK)
        return Response({"error": "Failed to fetch games."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)