from django.db import models
from django.db.models import Q, F, FloatField, Count, Sum, IntegerField, Value, DecimalField
from django.db.models.functions import Cast, Upper, Lower, Substr, Concat


class PlayerManager(models.QuerySet):
    def add_n_wins(self):
        return self.annotate(
            n_wins=Count('gameplayerrelationship__game__gameattribute',
                         filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome') &
                                Q(gameplayerrelationship__game__gameattribute__val='1'))
        )

    def add_n_games(self):
        return self.annotate(
            n_games=Count('gameplayerrelationship__game',
                          filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome'))
        )

    def add_n_ranked(self):
        return self.annotate(
            n_ranked=Count('gameplayerrelationship__game',
                           filter=Q(gameplayerrelationship__game__gameattribute__attr='ranked_status') &
                                  Q(gameplayerrelationship__game__gameattribute__val='1'))
        )

    def add_n_unranked(self):
        return self.annotate(
            n_unranked=Count('gameplayerrelationship__game',
                             filter=Q(gameplayerrelationship__game__gameattribute__attr='ranked_status') &
                                    Q(gameplayerrelationship__game__gameattribute__val='0'))
        )

    def add_pct_win(self):
        return self.annotate(
            pct_win=Cast(Cast(Value(100) * F('n_wins'), FloatField()) / Cast(F('n_games'), FloatField()),
                         DecimalField(decimal_places=2))
        )

    def add_player_tidy(self):
        return self.annotate(
            player_tidy=Concat(Upper(Substr('player_name', 1, 1)), Lower(Substr('player_name', 2)))
        )


class Player(models.Model):
    player_name = models.CharField(max_length=200)

    objects = PlayerManager.as_manager()

    def __str__(self):
        return self.player_name


class GameSet(models.QuerySet):
    def add_n_wins(self):
        return self.annotate(
            n_wins=Sum(Cast(F('gameattribute__val'), IntegerField()),
                       filter=Q(gameattribute__attr='game_outcome'))
        )

        # n_wins=Window(
        #     expression=Sum(Cast(F('gameattribute__val'), IntegerField()),
        #                    filter=Q(gameattribute__attr='game_outcome')),
        #     partition_by=['gameplayerrelationship__player'],
        #     order_by=['game_id'],
        #     frame=RowRange(start=-10, end=1)
        # )

        # def add_player(self):
        #     return self.annotate(
        #         player=Substr('gameplayerrelationship__player__player_name', 1)
        #     )


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)

    objects = GameSet.as_manager()

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


class GamePlayerRelationshipSet(models.QuerySet):
    def add_n_wins(self):
        return self.annotate(
            n_wins=Sum(Cast(F('game__gameattribute__val'), IntegerField()),
                       filter=Q(game__gameattribute__attr='game_outcome'))
        )


class GamePlayerRelationship(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    objects = GamePlayerRelationshipSet.as_manager()

    def __str__(self):
        return self.game, self.player
