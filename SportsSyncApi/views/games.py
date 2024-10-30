from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from datetime import datetime, timedelta
from .utils import get_custom_headers

class GamesAPI:
    @staticmethod
    def get_games():
        try:
            live_games, upcoming_games, recent_games = [], [], []
            board = scoreboard.ScoreBoard()
            data = board.get_dict()
            
            if 'scoreboard' in data and 'games' in data['scoreboard']:
                games = data['scoreboard']['games']
                print(f"Found {len(games)} games")
                
                for game in games:
                    game_data = GamesAPI._format_game_data(game)
                    
                    if game['period'] > 0 and game['gameStatus'] != 3:
                        live_games.append(game_data)
                    elif game['gameStatus'] == 3:
                        recent_games.append(game_data)
                    else:
                        upcoming_games.append(game_data)

            return {'live_games': live_games, 'upcoming_games': upcoming_games, 'recent_games': recent_games}
            
        except Exception as e:
            print(f"Error in get_games: {str(e)}")
            return {'live_games': [], 'upcoming_games': [], 'recent_games': []}

    @staticmethod
    def get_game_details(game_id):
        try:
            board = scoreboard.ScoreBoard()
            games = board.get_dict()['scoreboard']['games']
            game_basic = next((g for g in games if g['gameId'] == game_id), None)

            if not game_basic:
                return None

            box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            box_score_data = box_score.get_dict()

            return {
                'basic_info': GamesAPI._format_game_data(game_basic),
                'box_score': {
                    'home_team_stats': box_score_data.get('HomeTeamStats', []),
                    'away_team_stats': box_score_data.get('AwayTeamStats', []),
                    'player_stats': box_score_data.get('PlayerStats', [])
                }
            }
        except Exception as e:
            print(f"Error getting game details: {str(e)}")
            return None

    @staticmethod
    def _format_game_data(game):
        return {
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

class GamesScheduleAPI:
    @staticmethod
    def get_games_by_date(date='today'):
        try:
            date_offset = {
                'yesterday': -1,
                'today': 0,
                'tomorrow': 1
            }.get(date, 0)
            
            target_date = datetime.now() + timedelta(days=date_offset)
            board = scoreboard.ScoreBoard(game_date=target_date.strftime('%Y-%m-%d'))
            data = board.get_dict()
            
            live_games, upcoming_games, recent_games = [], [], []
            
            if 'scoreboard' in data and 'games' in data['scoreboard']:
                games = data['scoreboard']['games']
                print(f"Found {len(games)} games for {target_date.strftime('%Y-%m-%d')}")
                
                for game in games:
                    game_data = GamesAPI._format_game_data(game)
                    
                    if game['period'] > 0 and game['gameStatus'] != 3:
                        live_games.append(game_data)
                    elif game['gameStatus'] == 3:
                        recent_games.append(game_data)
                    else:
                        upcoming_games.append(game_data)

            return {'live_games': live_games, 'upcoming_games': upcoming_games, 'recent_games': recent_games}
                
        except Exception as e:
            print(f"Error in get_games_by_date: {str(e)}")
            return {'live_games': [], 'upcoming_games': [], 'recent_games': []}

class GamesView(APIView):
    def get(self, request):
        games = GamesAPI.get_games()
        return Response(games, status=status.HTTP_200_OK)

class GamesScheduleView(APIView):
    def get(self, request):
        date = request.query_params.get('date', 'today')
        games = GamesScheduleAPI.get_games_by_date(date)
        return Response(games, status=status.HTTP_200_OK)

class GameDetailsView(APIView):
    def get(self, request, game_id):
        game_details = GamesAPI.get_game_details(game_id)
        if game_details:
            return Response(game_details)
        return Response({"error": "Game not found"}, status=404)

class HistoricalMatchupsView(APIView):
    def get(self, request):
        team1_id = request.GET.get('team1')
        team2_id = request.GET.get('team2')
        if not team1_id or not team2_id:
            return Response({"error": "Both team IDs required"}, status=400)
        matchups = GamesAPI.get_historical_matchups(team1_id, team2_id)
        return Response(matchups)