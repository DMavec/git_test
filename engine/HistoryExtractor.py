import re
import sys
import pandas as pd
import engine.constants as consts
from engine.RiotAPI import RiotAPI
from api.models import Game, Player, GamePlayerRelationship, GameAttribute


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
            Warning('Non-classic game')
            return []
    except:
        #TODO: Read up on exceptions and make this better
        Exception('Unexpected error with data checking in extract_game:', sys.exc_info()[0])

    players = [re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()
               for participantIdentity
               in match_details['participantIdentities']]
    team = [player for player in players if player in summoner_names]

    # Identify which participant id matches the summoner name
    pid = [participantIdentity['participantId']
           for participantIdentity
           in match_details['participantIdentities']
           if team[0] in re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()]

    win_status = int([x['stats']['win']
                      for x in match_details['participants']
                      if x['participantId'] == pid[0]][0])
    ranked_status = int(len(match_details['teams'][0]['bans']) > 0)

    for team_player in team:
        return [(game_id, team_player, ts, '|'.join(team), win_status, ranked_status)]


def extract_games(api, summoner_names, new_game_ids):
    if len(new_game_ids) == 0:
        Warning('No new data to load')
    else:
        game_data = []
        for (game_id, ts) in list(new_game_ids)[0:5]:
            game_data += extract_game(api, summoner_names, game_id, ts)

        return game_data


## Transform data

## Load data
# TODO: Replace with an update_or_create directly into database

def test_load():
    # Initialise API
    api = RiotAPI(consts.API_KEY)

    # Get summoner names
    summoner_names = consts.SUMMONER_NAMES
    account_ids = get_account_ids(api, summoner_names)

    loaded_games = get_loaded_game_ids()
    new_games = get_new_game_ids(api, account_ids, loaded_games)
    game_data = extract_games(api, summoner_names, new_games)
    print(game_data)


class HistoryExtractor(object):
    def __init__(self, api, summoner_names):
        self.api = api
        self.summoner_names = [name.lower() for name in summoner_names]
        self.account_ids = [api.get_summoner_by_name(name)['accountId'] for name in self.summoner_names]
        self.old_ids = consts.OLD_IDS.drop_duplicates('game_id', keep='last')['game_id'].tolist()
        self.game_ids = []
        self.skipped_ids = []
        self.extract_data = {'game_id': [], 'attribute': [], 'value': []}
        self.load_data = pd.DataFrame()
        self.game_log = []
        self.new_data = False

    def _extract_timestamp(self, match):
        if not match['gameId'] in self.extract_data['game_id']:
            self.extract_data['game_id'] += [match['gameId']]
            self.extract_data['attribute'] += ['timestamp']
            self.extract_data['value'] += [match['timestamp']]

    def identify_new_games(self, full_load=False):
        if full_load:
            for account_id in self.account_ids:
                begin_index = 0
                n_records = 1
                while n_records > 0:
                    match_history = self.api.get_recent_matches(account_id, begin_index)['matches']
                    n_records = len(match_history)
                    begin_index += 100
                    for match in match_history:
                        self._extract_timestamp(match)
        else:
            for account_id in self.account_ids:
                match_history = self.api.get_recent_matches(account_id, begin_index=0)['matches']
                for match in match_history:
                    game_id = match['gameId']
                    if game_id not in self.old_ids:
                        self._extract_timestamp(match)

        self.game_ids = pd.Series(self.extract_data['game_id']).drop_duplicates().tolist()

    def extract(self):
        if len(self.game_ids) == 0:
            return 'No data to load'  # TODO: Change to a warning message
        else:
            for game_id in self.game_ids:
                self._extract_by_game_id(game_id)

    def _extract_by_game_id(self, game_id):
        match_details = self.api.get_match(game_id)
        try:
            if match_details is None:
                return 'request fail'

            if match_details['gameMode'] != 'CLASSIC':
                self.skipped_ids += [game_id]
                return 'skip'
        except:
            # TODO: Throw as an actual exception. Wrap iterator in try / except loop if I want it to continue.
            print('Unexpected error with data checking in _extract_by_game_id:', sys.exc_info()[0])

        players = [re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()
                   for participantIdentity
                   in match_details['participantIdentities']]
        team = [player for player in players if player in self.summoner_names]

        # Identify which participant id matches the summoner name
        pid = [participantIdentity['participantId']
               for participantIdentity
               in match_details['participantIdentities']
               if team[0] in re.sub('[\s+]', '', participantIdentity['player']['summonerName']).lower()]

        win_status = int([x['stats']['win']
                          for x in match_details['participants']
                          if x['participantId'] == pid[0]][0])
        ranked_status = int(len(match_details['teams'][0]['bans']) > 0)

        data_attribute = ['player' + str(x) for x in list(range(0, len(team)))]
        data_value = team

        data_attribute.extend(['game_outcome', 'ranked_status'])
        data_value.extend([str(win_status), str(ranked_status)])

        # TODO: Replace with an update_or_create directly into database
        self.extract_data['game_id'] += [game_id] * len(data_attribute)
        self.extract_data['attribute'] += data_attribute
        self.extract_data['value'] += data_value

        return 'run'

    def load(self, file_name):
        self.load_data = (pd.DataFrame(self.extract_data)
                          .reindex(columns=['game_id', 'attribute', 'value'])
                          .drop_duplicates()
                          )

        if len(self.load_data) > 0:
            game_log = (self.load_data[self.load_data.attribute.str.contains('player[0-9]?')]
                        .filter(['game_id', 'value']))
            skipped_log = pd.DataFrame({'game_id': self.skipped_ids,
                                        'value': [''] * len(self.skipped_ids)})
            game_log = pd.concat([game_log, skipped_log])

            pd.DataFrame.to_csv(self.load_data, file_name,
                                mode='a', header=False, index=False, encoding='utf-8')
            pd.DataFrame.to_csv(game_log, 'data/game_log.csv',
                                mode='a', header=False, index=False, encoding='utf-8')

            self.load_data = pd.read_csv(file_name)
            self.game_log = pd.read_csv('data/game_log.csv')
            self.new_data = True
