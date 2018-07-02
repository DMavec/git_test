from django.db import models
from django.db.models import Q, F, FloatField, Count, Sum, Value, DecimalField
from django.db.models.functions import Cast


class PlayerManager(models.QuerySet):
    def annotate_fields(self):
        return self.annotate(
            n_wins=Sum('game__game_outcome'),
            n_games=Count('game'),
            n_ranked=Sum('game__ranked_status'),
            n_unranked=F('n_games') - F('n_ranked'),
            pct_win=Cast(Cast(Value(100) * F('n_wins'), FloatField()) / Cast(F('n_games'), FloatField()),
                         DecimalField(decimal_places=2))
        ).order_by('-n_wins')


class Player(models.Model):
    player_name = models.CharField(primary_key=True, max_length=200)
    account_id = models.IntegerField(default=-999)

    objects = PlayerManager.as_manager()

    def __str__(self):
        return self.player_name


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    player = models.ManyToManyField(Player)
    ts = models.DateTimeField(default='1970-01-01 00:00:00')
    game_outcome = models.IntegerField(default=0)
    ranked_status = models.IntegerField(default=0)
    players = models.CharField(max_length=1000, default='NULL')

    def __str__(self):
        template = '{0.game_id}'
        return template.format(self)