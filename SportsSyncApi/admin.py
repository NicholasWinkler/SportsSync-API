from django.contrib import admin
from .models.favorite_team import FavoriteTeam
from .models.team import TeamListTeam
from .models.team import TeamListPlayer

admin.site.register(FavoriteTeam)
admin.site.register(TeamListTeam)
admin.site.register(TeamListPlayer)