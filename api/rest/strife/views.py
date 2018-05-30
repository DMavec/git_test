# Models
from strife.models import Player, GamePlayerRelationship
from django.contrib.auth.models import User
# Serializers
from strife.serializers import PlayerSerializer, UserSerializer, GameSerializer, GamePlayerSerializer
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
            annotate_fields().\
            order_by('-pct_win')


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = GamePlayerRelationship.objects.all()
    serializer_class = GamePlayerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('player__player_name', )

    def get_queryset(self):
        queryset = GamePlayerRelationship.objects.all()
        queryset = queryset.select_related('game', 'player')
        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

