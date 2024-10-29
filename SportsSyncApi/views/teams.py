from nba_api.stats.endpoints import leaguestandings
from .utils import get_custom_headers

class TeamsAPI:
    @staticmethod
    def get_standings():
        """Get current NBA standings"""
        try:
            standings = leaguestandings.LeagueStandings(
                headers=get_custom_headers()
            ).get_dict()
            
            east = []
            west = []
            
            if standings['resultSets'][0]['rowSet']:
                for team in standings['resultSets'][0]['rowSet']:
                    team_data = {
                        'team': team[4],     # Team name
                        'wins': int(team[12]),
                        'losses': int(team[13]),
                        'streak': team[36].strip()   # Current streak (trimmed)
                    }
                    
                    if team[5] == 'East':
                        east.append(team_data)
                    else:
                        west.append(team_data)
                
                # Sort by wins
                east.sort(key=lambda x: (-x['wins'], x['losses']))
                west.sort(key=lambda x: (-x['wins'], x['losses']))
            
            return {
                'east': east,
                'west': west
            }
            
        except Exception as e:
            print(f"Error fetching standings: {str(e)}")
            return {'east': [], 'west': []}