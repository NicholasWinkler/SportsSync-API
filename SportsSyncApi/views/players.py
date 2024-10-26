# apps/nba/views/players.py
from urllib.request import urlopen
import json
from django.http import JsonResponse

def get_players(request):
    """Get player statistics"""
    try:
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 25)
        
        url = f"https://www.balldontlie.io/api/v1/players?page={page}&per_page={per_page}"
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_player_stats(request, player_id):
    """Get statistics for a specific player"""
    try:
        url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}"
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
