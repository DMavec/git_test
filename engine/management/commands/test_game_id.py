from django.core.management.base import BaseCommand, CommandError
from engine.etl import extract_games, load_games, get_account_ids, get_loaded_game_ids, get_new_game_ids
from engine.RiotAPI import RiotAPI
import engine.constants as consts


class Command(BaseCommand):
    help = '''Loads new game data into the api.
      full_load: default false
      Run on all available data from api. By default only checks the last 100 games.'''

    def handle(self, *args, **options):
        # Initialise API
        api = RiotAPI(consts.API_KEY)

        # Get summoner names
        summoner_names = consts.SUMMONER_NAMES
        account_ids = get_account_ids(api, summoner_names)

        new_games = [game for game in get_new_game_ids(api, account_ids, []) if game[0] == 148825668]
        print(new_games)
        game_data = extract_games(api, summoner_names, new_games)
        print(game_data)
        load_games(game_data)