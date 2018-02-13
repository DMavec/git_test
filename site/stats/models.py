from django.db import models

# Create your models here.
class Players(models.Model):
    player_name = models.CharField(max_length=200)

    def __str__(self):
        return self.player_name

class Games(models.Model):
    game_id = models.IntegerField()
    attribute = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.attribute, self.value

