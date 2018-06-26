from django.core.management.base import BaseCommand, CommandError
from engine.etl import run_etl


class Command(BaseCommand):
    help = 'Adds past game ids to the db'

    def handle(self, *args, **options):
        run_etl()