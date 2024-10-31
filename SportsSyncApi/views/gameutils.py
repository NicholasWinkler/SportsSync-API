import time
import requests
from functools import wraps
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls=20, per=60):
        self.calls = calls
        self.per = per
        self.timestamps = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < self.per]
            
            if len(self.timestamps) >= self.calls:
                sleep_time = self.timestamps[0] + self.per - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            self.timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper

# Fallback API (balldontlie)
class BallDontLieAPI:
    BASE_URL = "https://www.balldontlie.io/api/v1"
    
    @staticmethod
    def get_games():
        try:
            response = requests.get(f"{BallDontLieAPI.BASE_URL}/games")
            if response.status_code == 200:
                return response.json()
        except:
            return None
        return None

    @staticmethod
    def get_game_stats(game_id):
        try:
            response = requests.get(f"{BallDontLieAPI.BASE_URL}/stats?game_ids[]={game_id}")
            if response.status_code == 200:
                return response.json()
        except:
            return None
        return None

# Sample data for testing
SAMPLE_GAMES_DATA = {
    "games": [
        {
            "gameId": "0022300737",
            "homeTeam": {
                "teamId": "1610612744",
                "teamName": "Golden State Warriors",
                "score": 120
            },
            "awayTeam": {
                "teamId": "1610612747",
                "teamName": "Los Angeles Lakers",
                "score": 115
            },
            "gameStatus": 3,
            "gameStatusText": "Final",
            "period": 4,
            "gameClock": "",
            "gameTimeUTC": "2024-02-01T03:00:00Z"
        },
        # Add more sample games...
    ]
}

SAMPLE_GAMES_DATA = {
    "games": [
        {
            "game_id": "0022300001",
            "home_team": {
                "team_id": "1610612744",
                "team_name": "Golden State Warriors",
                "score": 0
            },
            "away_team": {
                "team_id": "1610612747",
                "team_name": "Los Angeles Lakers",
                "score": 0
            },
            "game_status": 1,
            "game_status_text": "Scheduled",
            "period": 0,
            "game_clock": "",
            "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        {
            "game_id": "0022300002",
            "home_team": {
                "team_id": "1610612738",
                "team_name": "Boston Celtics",
                "score": 112
            },
            "away_team": {
                "team_id": "1610612751",
                "team_name": "Brooklyn Nets",
                "score": 109
            },
            "game_status": 3,
            "game_status_text": "Final",
            "period": 4,
            "game_clock": "",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        {
            "game_id": "0022300003",
            "home_team": {
                "team_id": "1610612748",
                "team_name": "Miami Heat",
                "score": 85
            },
            "away_team": {
                "team_id": "1610612755",
                "team_name": "Philadelphia 76ers",
                "score": 82
            },
            "game_status": 2,
            "game_status_text": "3rd Quarter",
            "period": 3,
            "game_clock": "5:30",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    ]
}

# Updated sample stats with more realistic data
SAMPLE_STATS_DATA = {
    "game_info": {
        "status": "Final",
        "period": 4,
        "game_clock": "",
        "arena": "Chase Center",
        "city": "San Francisco",
        "attendance": 18064,
    },
    "home_team": {
        "team_info": {
            "team_id": "1610612744",
            "team_name": "Golden State Warriors",
            "team_city": "Golden State",
            "team_tricode": "GSW",
        },
        "basic": {
            "points": 120,
            "assists": 25,
            "rebounds": 45,
            "steals": 8,
            "blocks": 5,
            "turnovers": 12,
            "fg_made": 45,
            "fg_attempted": 89,
            "fg_pct": 48.8,
            "ft_made": 20,
            "ft_attempted": 25,
            "ft_pct": 85.0,
            "fg3_made": 15,
            "fg3_attempted": 35,
            "fg3_pct": 37.5
        },
        "players": [
            {
                "player_id": "201939",
                "name": "Stephen Curry",
                "position": "PG",
                "jersey_num": "30",
                "starter": True,
                "minutes": "35:22",
                "points": 32,
                "assists": 8,
                "rebounds": 5,
                "steals": 2,
                "blocks": 0,
                "turnovers": 3,
                "fg_made": 12,
                "fg_attempted": 22,
                "fg_pct": 52.4,
                "ft_made": 5,
                "ft_attempted": 6,
                "ft_pct": 90.0,
                "fg3_made": 6,
                "fg3_attempted": 12,
                "fg3_pct": 50.0,
                "plus_minus": "+15"
            },
            {
                "player_id": "203110",
                "name": "Klay Thompson",
                "position": "SG",
                "jersey_num": "11",
                "starter": True,
                "minutes": "32:15",
                "points": 25,
                "assists": 3,
                "rebounds": 4,
                "steals": 1,
                "blocks": 0,
                "turnovers": 2,
                "fg_made": 9,
                "fg_attempted": 18,
                "fg_pct": 50.0,
                "ft_made": 2,
                "ft_attempted": 2,
                "ft_pct": 100.0,
                "fg3_made": 5,
                "fg3_attempted": 10,
                "fg3_pct": 50.0,
                "plus_minus": "+12"
            }
        ]
    },
    "away_team": {
        "team_info": {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "team_city": "Los Angeles",
            "team_tricode": "LAL",
        },
        "basic": {
            "points": 115,
            "assists": 22,
            "rebounds": 40,
            "steals": 6,
            "blocks": 4,
            "turnovers": 14,
            "fg_made": 42,
            "fg_attempted": 86,
            "fg_pct": 46.5,
            "ft_made": 18,
            "ft_attempted": 22,
            "ft_pct": 82.0,
            "fg3_made": 12,
            "fg3_attempted": 32,
            "fg3_pct": 35.0
        },
        "players": [
            {
                "player_id": "2544",
                "name": "LeBron James",
                "position": "SF",
                "jersey_num": "23",
                "starter": True,
                "minutes": "38:15",
                "points": 28,
                "assists": 11,
                "rebounds": 8,
                "steals": 1,
                "blocks": 1,
                "turnovers": 4,
                "fg_made": 11,
                "fg_attempted": 22,
                "fg_pct": 50.0,
                "ft_made": 4,
                "ft_attempted": 5,
                "ft_pct": 85.0,
                "fg3_made": 2,
                "fg3_attempted": 6,
                "fg3_pct": 33.3,
                "plus_minus": "-8"
            }
        ]
    }
}

def get_game_status_text(status_code):
    """Convert status code to readable text"""
    STATUS_MAPPING = {
        1: "Scheduled",
        2: "In Progress",
        3: "Final",
        4: "Postponed",
        5: "Cancelled"
    }
    return STATUS_MAPPING.get(status_code, "Unknown")