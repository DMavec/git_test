from django.core.management.base import BaseCommand, CommandError
from engine.backup import restore

class Command(BaseCommand):
    help = 'Backup database to Google Drive.'

    def handle(self, *args, **options):
        restore()