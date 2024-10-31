# views/teamlist.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nba_api.stats.endpoints import LeagueDashPlayerStats, LeagueStandings

# Team ID to nickname mapping with logo URLs
TEAM_MAPPING = {
    1: {
        'nickname': 'Cavaliers',
        'abbreviation': 'CLE',
        'logo': 'https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg'
    },
    2: {
        'nickname': 'Celtics',
        'abbreviation': 'BOS',
        'logo': 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg'
    },
    3: {
        'nickname': 'Bulls',
        'abbreviation': 'CHI',
        'logo': 'https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg'
    },
    4: {
        'nickname': 'Magic',
        'abbreviation': 'ORL',
        'logo': 'https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg'
    },
    5: {
        'nickname': 'Knicks',
        'abbreviation': 'NYK',
        'logo': 'https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg'
    },
    6: {
        'nickname': 'Heat',
        'abbreviation': 'MIA',
        'logo': 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg'
    },
    7: {
        'nickname': 'Hornets',
        'abbreviation': 'CHA',
        'logo': 'https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg'
    },
    8: {
        'nickname': 'Wizards',
        'abbreviation': 'WAS',
        'logo': 'https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg'
    },
    9: {
        'nickname': 'Hawks',
        'abbreviation': 'ATL',
        'logo': 'https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg'
    },
    10: {
        'nickname': 'Nets',
        'abbreviation': 'BKN',
        'logo': 'https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg'
    },
    11: {
        'nickname': 'Pacers',
        'abbreviation': 'IND',
        'logo': 'https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg'
    },
    12: {
        'nickname': 'Bucks',
        'abbreviation': 'MIL',
        'logo': 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg'
    },
    13: {
        'nickname': '76ers',
        'abbreviation': 'PHI',
        'logo': 'https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg'
    },
    14: {
        'nickname': 'Raptors',
        'abbreviation': 'TOR',
        'logo': 'https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg'
    },
    15: {
        'nickname': 'Pistons',
        'abbreviation': 'DET',
        'logo': 'https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg'
    },
    16: {
        'nickname': 'Thunder',
        'abbreviation': 'OKC',
        'logo': 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg'
    },
    17: {
        'nickname': 'Warriors',
        'abbreviation': 'GSW',
        'logo': 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg'
    },
    18: {
        'nickname': 'Suns',
        'abbreviation': 'PHX',
        'logo': 'https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg'
    },
    19: {
        'nickname': 'Mavericks',
        'abbreviation': 'DAL',
        'logo': 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg'
    },
    20: {
        'nickname': 'Lakers',
        'abbreviation': 'LAL',
        'logo': 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg'
    },
    21: {
        'nickname': 'Clippers',
        'abbreviation': 'LAC',
        'logo': 'https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg'
    },
    22: {
        'nickname': 'Timberwolves',
        'abbreviation': 'MIN',
        'logo': 'https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg'
    },
    23: {
        'nickname': 'Kings',
        'abbreviation': 'SAC',
        'logo': 'https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg'
    },
    24: {
        'nickname': 'Nuggets',
        'abbreviation': 'DEN',
        'logo': 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg'
    },
    25: {
        'nickname': 'Rockets',
        'abbreviation': 'HOU',
        'logo': 'https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg'
    },
    26: {
        'nickname': 'Trail Blazers',
        'abbreviation': 'POR',
        'logo': 'https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg'
    },
    27: {
        'nickname': 'Pelicans',
        'abbreviation': 'NOP',
        'logo': 'https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg'
    },
    28: {
        'nickname': 'Grizzlies',
        'abbreviation': 'MEM',
        'logo': 'https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg'
    },
    29: {
        'nickname': 'Spurs',
        'abbreviation': 'SAS',
        'logo': 'https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg'
    },
    30: {
        'nickname': 'Jazz',
        'abbreviation': 'UTA',
        'logo': 'https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg'
    }
}

class TeamListView(APIView):
    def get(self, request):
        try:
            standings = LeagueStandings().get_dict()
            east_teams = []
            west_teams = []

            if standings['resultSets'][0]['rowSet']:
                for team in standings['resultSets'][0]['rowSet']:
                    team_name = team[4].split()[-1]
                    team_id = None
                    for id, info in TEAM_MAPPING.items():
                        if info['nickname'] == team_name:
                            team_id = id
                            break
                    
                    if team_id:
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
                            'win_pct': round(float(team[11]), 3) if team[11] != '' else 0.000,
                            'logo': TEAM_MAPPING[team_id]['logo']
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
            team_info = TEAM_MAPPING.get(int(team_id))
            if not team_info:
                return Response(
                    {'error': 'Team not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

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
                        'win_pct': round(float(team[11]), 3) if team[11] != '' else 0.000,
                        'logo': team_info['logo']
                    }
                    break

            players_data = LeagueDashPlayerStats().get_data_frames()[0]
            roster = []

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