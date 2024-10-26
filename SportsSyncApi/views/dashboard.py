# apps/nba/views/dashboard.py
from urllib.request import urlopen
import json
from datetime import datetime
from django.http import JsonResponse

def get_standings(request):
    """Get NBA standings data"""
    try:
        with urlopen("https://www.balldontlie.io/api/v1/teams") as response:
            data = json.loads(response.read().decode())
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search(request):
    """Search players and teams"""
    query = request.GET.get('q', '')
    try:
        results = []
        if query:
            # Search players
            with urlopen(f"https://www.balldontlie.io/api/v1/players?search={query}") as players_response:
                players_data = json.loads(players_response.read().decode())
                
            # Search teams
            with urlopen(f"https://www.balldontlie.io/api/v1/teams?search={query}") as teams_response:
                teams_data = json.loads(teams_response.read().decode())
            
            # Format results
            for player in players_data.get('data', []):
                results.append({
                    'id': player['id'],
                    'name': player['first_name'] + ' ' + player['last_name'],
                    'type': 'Player'
                })
            
            for team in teams_data.get('data', []):
                results.append({
                    'id': team['id'],
                    'name': team['full_name'],
                    'type': 'Team'
                })
            
        return JsonResponse(results, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
