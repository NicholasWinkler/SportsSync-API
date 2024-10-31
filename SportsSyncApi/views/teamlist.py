# views/teamlist.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nba_api.stats.endpoints import LeagueDashPlayerStats, LeagueStandings

# Team ID to nickname mapping
TEAM_MAPPING = {
    1: {'nickname': 'Cavaliers', 'abbreviation': 'CLE'},
    2: {'nickname': 'Celtics', 'abbreviation': 'BOS'},
    3: {'nickname': 'Bulls', 'abbreviation': 'CHI'},
    4: {'nickname': 'Magic', 'abbreviation': 'ORL'},
    5: {'nickname': 'Knicks', 'abbreviation': 'NYK'},
    6: {'nickname': 'Heat', 'abbreviation': 'MIA'},
    7: {'nickname': 'Hornets', 'abbreviation': 'CHA'},
    8: {'nickname': 'Wizards', 'abbreviation': 'WAS'},
    9: {'nickname': 'Hawks', 'abbreviation': 'ATL'},
    10: {'nickname': 'Nets', 'abbreviation': 'BKN'},
    11: {'nickname': 'Pacers', 'abbreviation': 'IND'},
    12: {'nickname': 'Bucks', 'abbreviation': 'MIL'},
    13: {'nickname': '76ers', 'abbreviation': 'PHI'},
    14: {'nickname': 'Raptors', 'abbreviation': 'TOR'},
    15: {'nickname': 'Pistons', 'abbreviation': 'DET'},
    16: {'nickname': 'Thunder', 'abbreviation': 'OKC'},
    17: {'nickname': 'Warriors', 'abbreviation': 'GSW'},
    18: {'nickname': 'Suns', 'abbreviation': 'PHX'},
    19: {'nickname': 'Mavericks', 'abbreviation': 'DAL'},
    20: {'nickname': 'Lakers', 'abbreviation': 'LAL'},
    21: {'nickname': 'Clippers', 'abbreviation': 'LAC'},
    22: {'nickname': 'Timberwolves', 'abbreviation': 'MIN'},
    23: {'nickname': 'Kings', 'abbreviation': 'SAC'},
    24: {'nickname': 'Nuggets', 'abbreviation': 'DEN'},
    25: {'nickname': 'Rockets', 'abbreviation': 'HOU'},
    26: {'nickname': 'Trail Blazers', 'abbreviation': 'POR'},
    27: {'nickname': 'Pelicans', 'abbreviation': 'NOP'},
    28: {'nickname': 'Grizzlies', 'abbreviation': 'MEM'},
    29: {'nickname': 'Spurs', 'abbreviation': 'SAS'},
    30: {'nickname': 'Jazz', 'abbreviation': 'UTA'}
}

class TeamListView(APIView):
    def get(self, request):
        try:
            # Get standings data
            standings = LeagueStandings().get_dict()
            east_teams = []
            west_teams = []

            if standings['resultSets'][0]['rowSet']:
                for team in standings['resultSets'][0]['rowSet']:
                    team_name = team[4].split()[-1]  # Get team nickname
                    # Find team ID from mapping
                    team_id = None
                    for id, info in TEAM_MAPPING.items():
                        if info['nickname'] == team_name:
                            team_id = id
                            break
                    
                    if team_id:  # Only add teams that are in our mapping
                        team_data = {
                            'id': team_id,
                            'name': team_name,
                            'wins': int(team[12]) if team[12] != '' else 0,
                            'losses': int(team[13]) if team[13] != '' else 0,
                            'streak': str(team[36]).strip() if team[36] else '',
                            'conference': str(team[5]) if team[5] else '',
                            'division': str(team[6]) if team[6] else '',
                            'conference_rank': int(team[7]) if team[7] and team[7] != '' else 0,
                            'division_rank': int(team[8]) if team[8] and team[8] != '' else 0,
                            'win_pct': round(float(team[11]), 3) if team[11] != '' else 0.000
                        }

                        if team_data['conference'] == 'East':
                            east_teams.append(team_data)
                        elif team_data['conference'] == 'West':
                            west_teams.append(team_data)

            return Response({
                'east': sorted(east_teams, key=lambda x: (-x['wins'], x['losses'])),
                'west': sorted(west_teams, key=lambda x: (-x['wins'], x['losses']))
            })

        except Exception as e:
            print(f"Error details: {str(e)}")
            return Response(
                {'error': 'Team list unavailable'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class TeamDetailView(APIView):
    def get(self, request, team_id):
        try:
            # Get team info from mapping
            team_info = TEAM_MAPPING.get(int(team_id))
            if not team_info:
                return Response(
                    {'error': 'Team not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get standings data for team record
            standings = LeagueStandings().get_dict()
            team_standings = None

            for team in standings['resultSets'][0]['rowSet']:
                if team[4].endswith(team_info['nickname']):
                    team_standings = {
                        'id': team_id,
                        'name': team_info['nickname'],
                        'conference': str(team[5]) if team[5] else '',
                        'division': str(team[6]) if team[6] else '',
                        'wins': int(team[12]) if team[12] != '' else 0,
                        'losses': int(team[13]) if team[13] != '' else 0,
                        'streak': str(team[36]).strip() if team[36] else '',
                        'win_pct': round(float(team[11]), 3) if team[11] != '' else 0.000
                    }
                    break

            # Get player stats
            players_data = LeagueDashPlayerStats().get_data_frames()[0]
            roster = []

            # Match players by team abbreviation
            team_players = players_data[players_data['TEAM_ABBREVIATION'] == team_info['abbreviation']]
            
            for _, player in team_players.iterrows():
                player_data = {
                    'id': player['PLAYER_ID'],
                    'name': player['PLAYER_NAME'],
                    'stats': {
                        'games_played': int(player['GP']) if str(player['GP']).strip() != '' else 0,
                        'minutes': round(float(player['MIN']) if str(player['MIN']).strip() != '' else 0, 1),
                        'points': round(float(player['PTS']) if str(player['PTS']).strip() != '' else 0, 1),
                        'rebounds': round(float(player['REB']) if str(player['REB']).strip() != '' else 0, 1),
                        'assists': round(float(player['AST']) if str(player['AST']).strip() != '' else 0, 1),
                        'steals': round(float(player['STL']) if str(player['STL']).strip() != '' else 0, 1),
                        'blocks': round(float(player['BLK']) if str(player['BLK']).strip() != '' else 0, 1),
                        'field_goal_percentage': f"{round(float(player['FG_PCT'])*100 if str(player['FG_PCT']).strip() != '' else 0, 1)}%",
                        'three_point_percentage': f"{round(float(player['FG3_PCT'])*100 if str(player['FG3_PCT']).strip() != '' else 0, 1)}%",
                        'free_throw_percentage': f"{round(float(player['FT_PCT'])*100 if str(player['FT_PCT']).strip() != '' else 0, 1)}%"
                    }
                }
                roster.append(player_data)

            if team_standings:
                team_standings['roster'] = roster
                return Response(team_standings)
            else:
                return Response(
                    {'error': 'Team data not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            print(f"Error details: {str(e)}")
            return Response(
                {'error': 'Team data unavailable'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )