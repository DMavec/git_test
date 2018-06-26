from django.core.management.base import BaseCommand, CommandError
from engine.constants import SUMMONER_NAMES
from api.models import Player


class Command(BaseCommand):
    help = 'Adds players to the db'

    def handle(self, *args, **options):
        for name in SUMMONER_NAMES:
            obj, created = Player.objects.get_or_create(player_name=name)
            if created:
                print('Adding player: ', name)