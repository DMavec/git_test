import pandas as pd
import os
import r_consts as Consts
import re

class ETLByName(object):
    def __init__(self, summonerName, api):
        self.summonerName = summonerName.lower()
        self.api = api

        self.accountId = api.get_summoner_by_name(self.summonerName)['accountId']
        self.oldIds = Consts.OLD_IDS[Consts.OLD_IDS['main_player'] == self.summonerName]['game_id'].tolist()#Consts.OLD_IDS.filter(like=summonerName, axis='main_player')['game_id']  ## Don't know why this doesn't work...
        self.gameIds = []
        self.extract_data = {'game_id': [], 'main_player': [], 'win_status': [], 'team': []}
        self.transform_data = {}

    def extract(self):
        self.gameIds = [match['gameId'] for match in self.api.get_recent_matches(self.accountId)['matches'] if match['gameId'] not in self.oldIds]

        if len(self.gameIds) == 0:
            return 'No new data'
        else:
            [self._extract_by_gameid(gameId) for gameId in self.gameIds]

    def _extract_by_gameid(self, gameId):
        match_details = self.api.get_match(gameId)
        if match_details == None:
            return 'request fail'

        # Check if ranked game - non-ranked participants are anonymous
        # TODO: Find out if there is a better way to identify ranked games from the API
        if 'player' not in match_details['participantIdentities'][0].keys():
            return 'skip'

        team = [x['player']['summonerName'].lower() for x in match_details['participantIdentities']]

        pid = [x['participantId'] for x in match_details['participantIdentities'] if self.summonerName in re.sub('[\s+]', '', x['player']['summonerName']).lower()]
        win_status = [x['stats']['win'] for x in match_details['participants'] if x['participantId'] == pid[0]][0]

        self.extract_data['game_id'].append(gameId)
        self.extract_data['win_status'].append(win_status)
        self.extract_data['main_player'].append(self.summonerName)
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
        load_ids = pd.DataFrame.from_dict({'main_player': self.summonerName, 'game_ids': self.gameIds})

        pd.DataFrame.to_csv(self.transform_data, file_name, mode='a', header=column_flag, index=False)
        pd.DataFrame.to_csv(load_ids[['main_player', 'game_ids']], 'load_log.csv', mode='a', header=False, index=False)
