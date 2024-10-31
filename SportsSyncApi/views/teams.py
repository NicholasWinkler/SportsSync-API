# views/teams.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from nba_api.stats.endpoints import LeagueStandings

class TeamsAPI:
    @staticmethod
    def get_standings():
        """Get current NBA standings"""
        try:
            standings = LeagueStandings().get_dict()
            east, west = [], []

            if standings['resultSets'][0]['rowSet']:
                for team in standings['resultSets'][0]['rowSet']:
                    team_data = {
                        'id': team[0],        # Team ID
                        'team': team[4],      # Team name
                        'wins': int(team[12]),
                        'losses': int(team[13]),
                        'streak': team[36].strip()  # Current streak (trimmed)
                    }

                    if team[5] == 'East':
                        east.append(team_data)
                    else:
                        west.append(team_data)

                # Sort by wins
                east.sort(key=lambda x: (-x['wins'], x['losses']))
                west.sort(key=lambda x: (-x['wins'], x['losses']))

            return {'east': east, 'west': west}

        except Exception as e:
            print(f"Error fetching standings: {e}")
            return {'east': [], 'west': []}

class TeamListView(APIView):
    def get(self, request):
        standings = TeamsAPI.get_standings()
        return Response(standings, status=status.HTTP_200_OK)

class TeamProfileView(APIView):
    def get(self, request, team_id):
        try:
            headers = {
                'Authorization': f'Bearer {settings.BALLDONTLIE_API_KEY}'
            }
            # Fetch team stats using the BallDon'tLie API with timeout
            team_response = requests.get(f'https://www.balldontlie.io/api/v1/teams/{team_id}', headers=headers, timeout=5)
            stats_response = requests.get(f'https://www.balldontlie.io/api/v1/games?team_ids[]={team_id}', headers=headers, timeout=5)
            players_response = requests.get(f'https://www.balldontlie.io/api/v1/players?team_ids[]={team_id}', headers=headers, timeout=5)

            team_info = team_response.json().get('data', {})
            stats = stats_response.json().get('data', [])
            players = players_response.json().get('data', [])

            # Collect wins/losses
            wins = sum(1 for game in stats if game['home_team_id'] == team_id and game['home_team_score'] > game['visitor_team_score'])
            losses = len(stats) - wins

            # Combine team info and wins/losses
            result = {
                'team': team_info,
                'wins': wins,
                'losses': losses,
                'roster': players  # Add fetched roster here
            }

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.Timeout:
            return Response({'error': 'Request timed out'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")  # Log error for debugging
            return Response({'error': 'Failed to fetch data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
