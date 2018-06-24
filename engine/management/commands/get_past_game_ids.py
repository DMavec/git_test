from django.core.management.base import BaseCommand, CommandError
from api.models import Game

class Command(BaseCommand):
    help = 'Adds past game ids to the db'

    def handle(self, *args, **options):
        Game.objects.get_or_create(game_id=124)