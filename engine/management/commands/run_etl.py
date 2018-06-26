from django.core.management.base import BaseCommand, CommandError
from engine.etl import run_etl


class Command(BaseCommand):
    help = '''Loads new game data into the api.
      full_load: default false
      Run on all available data from api. By default only checks the last 100 games.'''

    def handle(self, *args, **options):


        run_etl()