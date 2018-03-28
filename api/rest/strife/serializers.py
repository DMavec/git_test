from rest_framework import serializers
from strife.models import Player
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')


class PlayerSerializer(serializers.ModelSerializer):
    player_tidy = serializers.CharField(max_length=200)
    n_wins = serializers.IntegerField()
    n_games = serializers.IntegerField()
    n_ranked = serializers.IntegerField()
    pct_win = serializers.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = Player
        fields = ('id', 'player_name', 'player_tidy', 'n_wins', 'n_games', 'n_ranked', 'pct_win')
