from django.db import models


class Player(models.Model):
    player_name = models.CharField(max_length=200)

    def __str__(self):
        return self.player_name


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.game_id


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


class PlayerSummary(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    n_games = models.IntegerField()
    n_wins = models.IntegerField()
    pct_win = models.DecimalField(max_digits=6, decimal_places=3, default=-1)

    def __str__(self):
        return self.player_name, self.games, self.wins, self.win_rate
