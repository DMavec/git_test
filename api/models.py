from django.db import models
from django.db.models import Q, F, FloatField, Count, Sum, IntegerField, Value, DecimalField
from django.db.models.functions import Cast, Upper, Lower, Substr, Concat


class PlayerManager(models.QuerySet):
    def annotate_fields(self):
        return self.annotate(
            n_wins=Count('gameplayerrelationship__game__gameattribute',
                         filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome') &
                                Q(gameplayerrelationship__game__gameattribute__val='1')),
            n_games=Count('gameplayerrelationship',
                          filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome')),
            n_ranked=Count('gameplayerrelationship__game',
                           filter=Q(gameplayerrelationship__game__gameattribute__attr='ranked_status') &
                                  Q(gameplayerrelationship__game__gameattribute__val='1')),
            n_unranked=F('n_games') - F('n_ranked'),
            pct_win=Cast(Cast(Value(100) * F('n_wins'), FloatField()) / Cast(F('n_games'), FloatField()),
                         DecimalField(decimal_places=2))
        )


class Player(models.Model):
    player_name = models.CharField(max_length=200)

    objects = PlayerManager.as_manager()

    def __str__(self):
        return self.player_name


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(default='1970-01-01 00:00:00')
    game_outcome = models.IntegerField(default=0)
    ranked_status = models.IntegerField(default=0)
    players = models.CharField(max_length=1000, default='NULL')

    def __str__(self):
        template = '{0.game_id}'
        return template.format(self)


class GameAttribute(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attr = models.CharField(max_length=200, default='NULL')
    val = models.CharField(max_length=200, default='NULL')

    def __str__(self):
        template = '{0.attr} {0.val}'
        return template.format(self)


class GamePlayerRelationship(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return self.game, self.player
