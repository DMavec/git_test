from django.core.management.base import BaseCommand, CommandError
from engine.constants import SUMMONER_NAMES, API_KEY
from api.models import Player
from engine.RiotAPI import RiotAPI


class Command(BaseCommand):
    help = 'Adds players to the db.'

    def handle(self, *args, **options):
        api = RiotAPI(API_KEY)

        for name in SUMMONER_NAMES:
            account_id = api.get_summoner_by_name(name)['accountId']

            obj, created = Player.objects.update_or_create(player_name=name)
            obj.account_id = account_id
            obj.save()
            print('Updating player', name, '\nAccount ID:', account_id)