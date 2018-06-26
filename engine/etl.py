import re
import sys
import pandas as pd
import engine.constants as consts
from engine.RiotAPI import RiotAPI
from api.models import Game, Player


## Get account IDs
def get_account_ids(api, summoner_names):
    return [api.get_summoner_by_name(name)['accountId'] for name in summoner_names]


## Get already loaded game IDs
def get_loaded_game_ids():
    return [game for game in Game.objects.all().values_list('game_id', flat=True)]


## Get list of new games to load
def get_new_game_ids(api, account_ids, loaded_games, full_load=False):
    match_list = []
    for account_id in account_ids:
        if full_load:
            begin_index = 0
            n_records = 1
            while n_records > 0:
                match_history = api.get_recent_matches(account_id, begin_index)['matches']
                n_records = len(match_history)
                begin_index += 100
                for match in match_history:
                    match_list += [(match['gameId'], match['timestamp'])]
        else:
            match_history = api.get_recent_matches(account_id, begin_index=0)['matches']
            for match in match_history:
                game_id = match['gameId']
                if game_id not in loaded_games:
                    match_list += [(match['gameId'], match['timestamp'])]
    return set(match_list)


## Extract data for new games
def extract_game(api, summoner_names, game_id, ts):
    try:
        match_details = api.get_match(game_id)
        if match_details is None:
            Warning('Request failed')
            return []
        elif match_details['gameMode'] != 'CLASSIC':
            return [([], {'game_id': game_id, 'ts': ts})]
    except:
        # TODO: Read up on exceptions and make this better
        Exception('Unexpected error with data checking in extract_game:', sys.exc_info()[0])

    players = [re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()
               for participantIdentity
               in match_details['participantIdentities']]
    team = [player for player in players if player in summoner_names]

    # Identify which participant id matches the summoner name
    participant_id = [participantIdentity['participantId']
                      for participantIdentity
                      in match_details['participantIdentities']
                      if team[0] in re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()]

    game_outcome = int([x['stats']['win']
                        for x in match_details['participants']
                        if x['participantId'] == participant_id[0]][0])
    ranked_status = int(len(match_details['teams'][0]['bans']) > 0)

    return [(team,
             {'game_id': game_id,
              'ts': pd.to_datetime(ts, unit='ms', utc=True),
              'game_outcome': game_outcome,
              'ranked_status': ranked_status,
              'players': '|'.join(team)})]


def extract_games(api, summoner_names, new_game_ids):
    if len(new_game_ids) == 0:
        Warning('No new data to load')
    else:
        game_data = []
        for (game_id, ts) in list(new_game_ids)[0:5]:
            game_data += extract_game(api, summoner_names, game_id, ts)

        return game_data


## Load data
def load_games(game_data):
    for (players, data) in game_data:
        game, created = Game.objects.get_or_create(**data)
        for player in players:
            game.player.add(Player.objects.get(player_name=player))
        game.save()


def run_etl():
    # Initialise API
    api = RiotAPI(consts.API_KEY)

    # Get summoner names
    summoner_names = consts.SUMMONER_NAMES
    account_ids = get_account_ids(api, summoner_names)

    loaded_games = get_loaded_game_ids()
    new_games = get_new_game_ids(api, account_ids, loaded_games)
    game_data = extract_games(api, summoner_names, new_games)
    load_games(game_data)


if __name__ == "__main__":
    run_etl()