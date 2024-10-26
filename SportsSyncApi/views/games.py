# apps/nba/views/games.py
from urllib.request import urlopen
import json
from datetime import datetime
from django.http import JsonResponse

def get_games(request):
    """Get games for a specific date range"""
    try:
        start_date = request.GET.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        end_date = request.GET.get('end_date', start_date)
        
        url = f"https://www.balldontlie.io/api/v1/games?start_date={start_date}&end_date={end_date}"
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_featured_games(request):
    """Get featured games for the dashboard"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"https://www.balldontlie.io/api/v1/games?dates[]={today}"
        
        with urlopen(url) as response:
            games_data = json.loads(response.read().decode()).get('data', [])
        
        formatted_games = [
            {
                'id': game['id'],
                'homeTeam': game['home_team']['full_name'],
                'awayTeam': game['visitor_team']['full_name'],
                'time': game['status'],
                'date': game['date']
            }
            for game in games_data[:5]  # Get top 5 games
        ]
        
        return JsonResponse(formatted_games, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
