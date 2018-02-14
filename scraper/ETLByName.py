import os, re, sys
import pandas as pd
from scraper import constants as consts

class ETLByName(object):
    def __init__(self, summoner_name, api):
        self.summoner_name = summoner_name.lower()
        self.api = api
        self.account_id = api.get_summoner_by_name(self.summoner_name)['accountId']
        self.old_ids = consts.OLD_IDS[consts.OLD_IDS['main_player'] == self.summoner_name]['game_id'].tolist()#consts.OLD_IDS.filter(like=summonerName, axis='main_player')['game_id']  ## Don't know why this doesn't work...
        self.game_ids = []
        self.extract_data = {'game_id': [], 'main_player': [], 'ranked_status': [], 'win_status': [], 'team': []}
        self.transform_data = {}

    def extract(self):
        self.game_ids = [match['gameId'] for match in self.api.get_recent_matches(self.account_id)['matches'] if match['gameId'] not in self.old_ids]

        if len(self.game_ids) == 0:
            return 'No new data'
        else:
            [self._extract_by_gameid(gameId) for gameId in self.game_ids]

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

        team = [re.sub('[\s+]', '', x['player']['summonerName']).lower() for x in match_details['participantIdentities']]

        pid = [x['participantId']
               for x in match_details['participantIdentities']
               if self.summoner_name in re.sub('[\s+]', '', x['player']['summonerName']).lower()]
        win_status = [x['stats']['win']
                      for x in match_details['participants']
                      if x['participantId'] == pid[0]][0]
        ranked_status = len(match_details['teams'][0]['bans']) == 0

        self.extract_data['game_id'].append(gameId)
        self.extract_data['win_status'].append(win_status)
        self.extract_data['ranked_status'].append(ranked_status)
        self.extract_data['main_player'].append(self.summoner_name)
        self.extract_data['team'].append(team)
        return 'run'

    def transform(self):
        df = pd.DataFrame.from_dict(self.extract_data)
        df_team = df.pop('team').apply(pd.Series)
        #new_cols = dict(item.split(':') for item in [str(x - 1) + ': \'player_\'' + str(x) for x in range(1,11)])

        df = pd.concat([df, df_team], axis=1)
        self.transform_data = df

    def load(self, file_name):
        column_flag = not os.path.isfile(file_name)
        load_ids = pd.DataFrame.from_dict({'game_id': self.game_ids, 'player_name': self.summoner_name})

        pd.DataFrame.to_csv(self.transform_data, file_name, mode='a', header=column_flag, index=False, encoding='utf-8')
        pd.DataFrame.to_csv(load_ids[['game_id', 'player_name']], 'data/load_log.csv', mode='a', header=False, index=False, encoding='utf-8')
