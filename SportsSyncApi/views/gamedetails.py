# gamedetails.py
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings

class BallDontLieAPI:
    """Helper class for balldontlie API interactions"""
    BASE_URL = "https://api.balldontlie.io/v1"
    TIMEOUT = 10

    @staticmethod
    def get_headers():
        return {
            "Authorization": settings.BALLDONTLIE_API_KEY
        }

    @staticmethod
    def get_games(params=None):
        """Get games with optional parameters"""
        try:
            response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/games",
                headers=BallDontLieAPI.get_headers(),
                params=params,
                timeout=BallDontLieAPI.TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            print(f"API Error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error fetching games: {str(e)}")
            return None

    @staticmethod
    def get_game(game_id):
        """Get specific game details"""
        try:
            response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/games/{game_id}",
                headers=BallDontLieAPI.get_headers(),
                timeout=BallDontLieAPI.TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            print(f"API Error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error fetching game: {str(e)}")
            return None
    @staticmethod
    def get_live_box_scores():
        """Get all live box scores"""
        try:
            response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/box_scores/live",
                headers=BallDontLieAPI.get_headers(),
                timeout=BallDontLieAPI.TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            print(f"API Error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error fetching live box scores: {str(e)}")
            return None

    @staticmethod
    def get_box_scores(game_id):
        """Get box scores for a specific game"""
        try:
            response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/box_scores",
                headers=BallDontLieAPI.get_headers(),
                params={'game_ids[]': game_id},
                timeout=BallDontLieAPI.TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            print(f"API Error: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            print(f"Error fetching box scores: {str(e)}")
            return None

class GameList(APIView):
    """List games endpoint"""
    def get(self, request):
        try:
            # Try cache first
            cache_key = 'games_list'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)

            # Build query parameters
            params = {}
            
            # Handle pagination
            if 'per_page' in request.query_params:
                params['per_page'] = min(int(request.query_params['per_page']), 100)
            else:
                params['per_page'] = 100

            if 'cursor' in request.query_params:
                params['cursor'] = request.query_params['cursor']

            # Handle date filtering
            today = datetime.now().date()
            if 'dates[]' in request.query_params:
                params['dates[]'] = request.query_params.getlist('dates[]')
            else:
                # Default to next 7 days if no dates specified
                dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
                params['dates[]'] = dates

            # Handle other filters
            if 'seasons[]' in request.query_params:
                params['seasons[]'] = request.query_params.getlist('seasons[]')
            if 'team_ids[]' in request.query_params:
                params['team_ids[]'] = request.query_params.getlist('team_ids[]')
            if 'postseason' in request.query_params:
                params['postseason'] = request.query_params['postseason']
            if 'start_date' in request.query_params:
                params['start_date'] = request.query_params['start_date']
            if 'end_date' in request.query_params:
                params['end_date'] = request.query_params['end_date']

            # Get games from API
            response_data = BallDontLieAPI.get_games(params)
            if not response_data:
                return Response({
                    'data': [],
                    'meta': {'next_cursor': None, 'per_page': params.get('per_page', 25)}
                })

            # Cache results
            cache.set(cache_key, response_data, settings.GAME_CACHE_TIMEOUT)
            return Response(response_data)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error fetching games'
            }, status=500)

class GameDetails(APIView):
    """Game details endpoint using box scores"""
    def get(self, request, game_id):
        try:
            # Try cache first
            cache_key = f'game_details_{game_id}'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)

            # First try live box scores
            headers = BallDontLieAPI.get_headers()
            live_response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/box_scores/live",
                headers=headers,
                timeout=BallDontLieAPI.TIMEOUT
            )

            if live_response.status_code == 200:
                live_data = live_response.json()
                # Try to find the game in live games
                game = next(
                    (g for g in live_data.get('data', []) if str(g['id']) == str(game_id)), 
                    None
                )
                if game:
                    # Cache for a short time if it's a live game
                    cache.set(cache_key, game, 60)  # Cache for 1 minute
                    return Response(game)

            # If not found in live games, try regular box scores
            response = requests.get(
                f"{BallDontLieAPI.BASE_URL}/box_scores",
                headers=headers,
                params={'game_ids[]': game_id},
                timeout=BallDontLieAPI.TIMEOUT
            )

            if response.status_code != 200:
                return Response({
                    'error': 'Game not found',
                    'message': 'Unable to fetch game details',
                    'status_code': response.status_code
                }, status=404)

            data = response.json()
            if not data.get('data'):
                return Response({
                    'error': 'Game not found',
                    'message': 'No data available for this game'
                }, status=404)

            # Get the first (and should be only) game from the response
            game_data = data['data'][0]

            # Cache based on game status
            if game_data['status'] == "Final":
                cache.set(cache_key, game_data, settings.STATS_CACHE_TIMEOUT)
            else:
                cache.set(cache_key, game_data, settings.GAME_CACHE_TIMEOUT)

            return Response(game_data)

        except requests.Timeout:
            return Response({
                'error': 'Request timeout',
                'message': 'The API request took too long to respond',
                'game_id': game_id
            }, status=504)
        except requests.RequestException as e:
            return Response({
                'error': 'API request failed',
                'message': str(e),
                'game_id': game_id
            }, status=502)
        except Exception as e:
            return Response({
                'error': 'Unexpected error',
                'message': str(e),
                'game_id': game_id
            }, status=500)