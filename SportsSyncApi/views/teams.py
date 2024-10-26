# apps/nba/views/teams.py
from urllib.request import urlopen
import json
from django.http import JsonResponse

def get_teams(request):
    """Get all NBA teams"""
    try:
        url = "https://www.balldontlie.io/api/v1/teams"
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_team_stats(request, team_id):
    """Get statistics for a specific team"""
    try:
        url = f"https://www.balldontlie.io/api/v1/games?team_ids[]={team_id}"
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
