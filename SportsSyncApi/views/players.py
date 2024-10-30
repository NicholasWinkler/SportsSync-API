from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.endpoints import CommonPlayerInfo, PlayerCareerStats, PlayerGameLogs
from ..serializers import PlayerListSerializer, PlayerDetailSerializer

class PlayerListView(APIView):
    def get(self, request):
        try:
            # Fetch player data from the API
            players_data = LeagueDashPlayerStats().get_data_frames()[0]
            players_list = []

            # Loop through the players data and create Player instances
            for player_data in players_data.to_dict(orient='records'):
                player = {
                    'player_id': player_data['PLAYER_ID'],
                    'player_name': player_data['PLAYER_NAME'],
                    'nickname': player_data.get('NICKNAME', ''),  # Default to empty string
                    'team_id': player_data['TEAM_ID'],
                    'team_abbreviation': player_data['TEAM_ABBREVIATION'],
                    'age': player_data.get('AGE', 0),  # Default to 0 if not found
                    'gp': player_data['GP'],  # Games Played
                    'w': player_data['W'],    # Wins
                    'l': player_data['L'],    # Losses
                    'w_pct': player_data['W_PCT'],  # Win Percentage
                    'min': player_data['MIN'],  # Minutes
                    'fgm': player_data['FGM'],  # Field Goals Made
                    'fga': player_data['FGA'],  # Field Goals Attempted
                    'fg_pct': player_data['FG_PCT'],  # Field Goal Percentage
                    'fg3m': player_data['FG3M'],  # 3-Point Field Goals Made
                    'fg3a': player_data['FG3A'],  # 3-Point Field Goals Attempted
                    'fg3_pct': player_data['FG3_PCT'],  # 3-Point Field Goal Percentage
                    'ftm': player_data['FTM'],  # Free Throws Made
                    'fta': player_data['FTA'],  # Free Throws Attempted
                    'ft_pct': player_data['FT_PCT'],  # Free Throw Percentage
                    'oreb': player_data['OREB'],  # Offensive Rebounds
                    'dreb': player_data['DREB'],  # Defensive Rebounds
                    'reb': player_data['REB'],    # Total Rebounds
                    'ast': player_data['AST'],    # Assists
                    'tov': player_data['TOV'],    # Turnovers
                    'stl': player_data['STL'],    # Steals
                    'blk': player_data['BLK'],    # Blocks
                    'pts': player_data['PTS'],     # Points
                    'plus_minus': player_data['PLUS_MINUS'],  # Plus/Minus
                }
                players_list.append(player)

            # Serialize the player data for the response
            serializer = PlayerListSerializer(players_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PlayerProfileView(APIView):
    def get(self, request, player_id):
        try:
            # Fetch player stats
            players_data = LeagueDashPlayerStats().get_data_frames()[0]
            player_data = players_data[players_data['PLAYER_ID'] == player_id]

            if player_data.empty:
                return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

            player_stats = player_data.to_dict(orient='records')[0]
            # Serialize the player stats for the response
            serializer = PlayerDetailSerializer(player_stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)