from django.db import models
from django.contrib.auth.models import User

class FavoriteTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_teams')
    team_id = models.IntegerField()  # This should match your TeamListTeam team_id
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'SportsSyncApi'
        unique_together = ['user', 'team_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - Team {self.team_id}"