import os, re, sys
import pandas as pd
from scraper import constants as consts


class HistoryExtractor(object):
    def __init__(self, summoner_names, api):
        self.summoner_names = [name.lower() for name in summoner_names]
        self.api = api
        self.account_ids = [api.get_summoner_by_name(name)['accountId'] for name in self.summoner_names]
        self.old_ids = consts.OLD_IDS.drop_duplicates('game_id', keep='last')['game_id'].tolist()
        self.game_ids = []
        self.extract_data = {'game_id': [], 'attribute': [], 'value': []}
        self.load_data = pd.DataFrame()

    def extract(self):
        self.game_ids = [match['gameId']
                         for match_history
                         in [self.api.get_recent_matches(account_id)['matches'] for account_id in self.account_ids]
                         for match
                         in match_history
                         if match['gameId'] not in self.old_ids]

        ## Used for running historical "catch-up" - should only be required once after migrating
        # self.game_ids = self.old_ids

        self.game_ids = pd.Series(self.game_ids).drop_duplicates().tolist()

        if len(self.game_ids) == 0:
            return 'No new data'
        else:
            [self._extract_by_gameid(gameId) for gameId in self.game_ids]
            self.load_data = pd.DataFrame.from_dict(self.extract_data). \
                reindex(columns=['game_id', 'attribute', 'value'])

    def _extract_by_gameid(self, gameId):
        match_details = self.api.get_match(gameId)
        try:
            if match_details == None:
                return 'request fail'

            if match_details['gameMode'] != 'CLASSIC':
                return 'skip'

        except:
            # print(match_details)
            print('Unexpected error with data checking in _extract_by_gameid:', sys.exc_info()[0])

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
        ranked_status = int(len(match_details['teams'][0]['bans']) == 0)

        data_attribute = ['player' + str(x) for x in list(range(0, len(team)))]
        data_value = team

        data_attribute.extend(['game_outcome', 'ranked_status'])
        data_value.extend([win_status, ranked_status])

        self.extract_data['game_id'].extend([gameId] * len(data_attribute))
        self.extract_data['attribute'].extend(data_attribute)
        self.extract_data['value'].extend(data_value)

        return 'run'

    def load(self, file_name):
        if len(self.load_data) > 0:
            game_log = self.load_data[self.load_data.attribute.str.contains('player[0-9]?')]. \
                filter(['game_id', 'value'])

            pd.DataFrame.to_csv(self.load_data, file_name,
                                mode='a', header=False, index=False, encoding='utf-8')
            pd.DataFrame.to_csv(game_log, 'scraper/data/game_log.csv',
                                mode='a', header=False, index=False, encoding='utf-8')
