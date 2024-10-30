from django.db import models

class Game(models.Model):
    game_id = models.CharField(max_length=20, primary_key=True)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)
    arena = models.CharField(max_length=100)
    broadcast = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'games'