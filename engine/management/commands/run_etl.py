from django.core.management.base import BaseCommand, CommandError
from engine.etl import run_etl


class Command(BaseCommand):
    help = '''Loads new game data into the api.
      full_load: default 0
      Set argument to 1 to run on all available data from api. By default only checks the last 100 games.'''

    def add_arguments(self, parser):
        parser.add_argument('full_load', nargs='+', type=bool,
                            help='Set to 1 to run on all available data from api. By default only checks the last 100 games.')

    def handle(self, *args, **options):
        run_etl(full_load=options['full_load'][0])
