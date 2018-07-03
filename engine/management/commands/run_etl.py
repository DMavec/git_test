from django.core.management.base import BaseCommand, CommandError
from engine.etl import run_etl


class Command(BaseCommand):
    help = 'Extracts, transforms and loads new game data into the api.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--full_load',
            action='store_true',
            dest='full_load',
            help='Run on all available data from Riot API instead of only checking for new games in the last 100.',
        )

    def handle(self, *args, **options):
        run_etl(full_load=options['full_load'])
