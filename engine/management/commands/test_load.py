from django.core.management.base import BaseCommand, CommandError
from engine.HistoryExtractor import test_load


class Command(BaseCommand):
    help = 'Adds past game ids to the db'

    def handle(self, *args, **options):
        test_load()