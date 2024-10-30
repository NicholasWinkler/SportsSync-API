from django.db import models

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    team_id = models.IntegerField()
    team_abbreviation = models.CharField(max_length=10)
    age = models.IntegerField(null=True, blank=True)
    gp = models.IntegerField()  # Games Played
    w = models.IntegerField()    # Wins
    l = models.IntegerField()    # Losses
    w_pct = models.FloatField()  # Win Percentage
    min = models.FloatField()    # Minutes
    fgm = models.IntegerField()  # Field Goals Made
    fga = models.IntegerField()  # Field Goals Attempted
    fg_pct = models.FloatField() # Field Goal Percentage
    fg3m = models.IntegerField() # 3-Point Field Goals Made
    fg3a = models.IntegerField() # 3-Point Field Goals Attempted
    fg3_pct = models.FloatField()# 3-Point Field Goal Percentage
    ftm = models.IntegerField()  # Free Throws Made
    fta = models.IntegerField()  # Free Throws Attempted
    ft_pct = models.FloatField() # Free Throw Percentage
    oreb = models.IntegerField() # Offensive Rebounds
    dreb = models.IntegerField() # Defensive Rebounds
    reb = models.IntegerField()   # Total Rebounds
    ast = models.IntegerField()   # Assists
    tov = models.IntegerField()   # Turnovers
    stl = models.IntegerField()   # Steals
    blk = models.IntegerField()   # Blocks
    pf = models.IntegerField()    # Personal Fouls
    pts = models.IntegerField()   # Points
    plus_minus = models.FloatField()  # Plus/Minus
    # Add any other fields that are necessary

    def __str__(self):
        return self.player_name