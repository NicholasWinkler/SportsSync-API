from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from datetime import datetime
from .utils import get_custom_headers

class PlayersAPI:
    @staticmethod
    def get_player_of_week():
        """Get Luka's current season stats"""
        try:
            # Find Luka Doncic
            player_list = players.find_players_by_full_name('Doncic')
            if not player_list:
                return None
                
            luka = next((p for p in player_list if p['full_name'] == 'Luka Doncic'), None)
            if not luka:
                return None

            # Get current season game log
            game_log = playergamelog.PlayerGameLog(
                player_id=luka['id'],
                season='2023-24',
                headers=get_custom_headers()
            ).get_dict()

            if not game_log['resultSets'][0]['rowSet']:
                return None

            # Calculate season averages
            games = game_log['resultSets'][0]['rowSet']
            games_played = len(games)
            
            if games_played == 0:
                return None

            stats = {
                'games': games_played,
                'points': sum(game[24] for game in games) / games_played,  # PTS
                'rebounds': sum(game[20] for game in games) / games_played,  # REB
                'assists': sum(game[21] for game in games) / games_played,  # AST
                'recent_games': []
            }

            # Add recent games
            for game in games[:5]:  # Last 5 games
                stats['recent_games'].append({
                    'date': game[3],      # GAME_DATE
                    'opponent': game[4],   # MATCHUP
                    'points': game[24],    # PTS
                    'rebounds': game[20],  # REB
                    'assists': game[21]    # AST
                })

            return {
                'name': 'Luka Dončić',
                'team': 'Dallas Mavericks',
                'stats': {
                    'points': round(stats['points'], 1),
                    'rebounds': round(stats['rebounds'], 1),
                    'assists': round(stats['assists'], 1),
                    'games_played': stats['games'],
                    'recent_games': stats['recent_games']
                }
            }

        except Exception as e:
            print(f"Error fetching player stats: {str(e)}")
            return None