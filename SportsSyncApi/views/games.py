from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timedelta
from .utils import get_custom_headers

class GamesAPI:
    @staticmethod
    def get_games():
        """Fetch both live/upcoming and recent games"""
        try:
            live_games = []
            upcoming_games = []
            recent_games = []

            # Get today's scoreboard
            board = scoreboard.ScoreBoard()
            data = board.get_dict()
            
            if 'scoreboard' in data and 'games' in data['scoreboard']:
                games = data['scoreboard']['games']
                print(f"Found {len(games)} games")
                
                for game in games:
                    game_data = {
                        'id': game['gameId'],
                        'status': game['gameStatusText'],
                        'date': game['gameEt'],
                        'time': game['gameStatusText'],
                        'home_team': {
                            'id': game['homeTeam']['teamId'],
                            'full_name': f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}",
                            'record': f"{game['homeTeam']['wins']}-{game['homeTeam']['losses']}",
                            'score': game['homeTeam'].get('score', 0)
                        },
                        'visitor_team': {
                            'id': game['awayTeam']['teamId'],
                            'full_name': f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}",
                            'record': f"{game['awayTeam']['wins']}-{game['awayTeam']['losses']}",
                            'score': game['awayTeam'].get('score', 0)
                        }
                    }
                    
                    # Print game data for debugging
                    print(f"Processing game: {game_data['home_team']['full_name']} vs {game_data['visitor_team']['full_name']}")
                    
                    if game['period'] > 0 and game['gameStatus'] != 3:  # Live game
                        live_games.append(game_data)
                    elif game['gameStatus'] == 3:  # Final
                        recent_games.append(game_data)
                    else:  # Upcoming
                        upcoming_games.append(game_data)

            print(f"Processed - Live: {len(live_games)}, Upcoming: {len(upcoming_games)}, Recent: {len(recent_games)} games")

            return {
                'live_games': live_games,
                'upcoming_games': upcoming_games,
                'recent_games': recent_games
            }
            
        except Exception as e:
            print(f"Error in get_games: {str(e)}")
            print(f"Error details:", e.__dict__)
            return {
                'live_games': [],
                'upcoming_games': [],
                'recent_games': []
            }