# Models
from strife.models import Player, GamePlayerRelationship
from django.contrib.auth.models import User
# Serializers
from strife.serializers import PlayerSerializer, UserSerializer, GameSerializer
# Permissions
# from strife.permissions import
# Rest Framework
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Player.objects.\
            add_n_wins(). \
            add_n_games(). \
            add_pct_win(). \
            add_n_ranked(). \
            add_n_unranked(). \
            order_by('-pct_win'). \
            add_player_tidy()


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = GamePlayerRelationship.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('player__player_name', )

    def get_queryset(self):
        queryset = GamePlayerRelationship.objects.all()
        queryset = queryset.select_related('game', 'player')
        queryset = queryset.add_n_wins().order_by('player_id', 'game_id')
        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer