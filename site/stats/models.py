from django.db import models


class Player(models.Model):
    player_name = models.CharField(max_length=200)

    def __str__(self):
        return self.player_name


class Game(models.Model):
    game_id = models.IntegerField()
    attr = models.CharField(max_length=200, default='NULL')
    val = models.CharField(max_length=200, default='NULL')

    def __str__(self):
        return self.attr, self.val


class GamePlayerRelationship(models.Model):
    game_id = models.IntegerField()
    player_name = models.CharField(max_length=200)

    def __str__(self):
        return self.game_id, self.player_name


class WinRate(models.Model):
    player_name = models.CharField(max_length=200)
    games = models.IntegerField()
    wins = models.IntegerField()
    win_rate = models.DecimalField(max_digits=6, decimal_places=3, default=-1)

    def __str__(self):
        return self.player_name, self.games, self.wins, self.win_rate