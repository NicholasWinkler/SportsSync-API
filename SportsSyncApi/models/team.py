from django.db import models

class TeamListTeam(models.Model):
    team_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)
    conference = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    class Meta:
        app_label = 'SportsSyncApi'

    def __str__(self):
        return self.full_name

class TeamListPlayer(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.CharField(max_length=3)
    position = models.CharField(max_length=5)
    team = models.ForeignKey(TeamListTeam, on_delete=models.CASCADE, related_name='players')
    age = models.IntegerField(null=True)
    gp = models.IntegerField(default=0)
    min = models.FloatField(default=0)
    pts = models.FloatField(default=0)
    reb = models.FloatField(default=0)
    ast = models.FloatField(default=0)
    stl = models.FloatField(default=0)
    blk = models.FloatField(default=0)

    class Meta:
        app_label = 'SportsSyncApi'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"