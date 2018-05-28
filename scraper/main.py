import os
if os.getcwd().endswith('riot_project'):
    os.chdir('scraper')

import pandas as pd

import constants as consts
from HistoryExtractor import HistoryExtractor
from RiotAPI import RiotAPI
from SiteDataLoader import SiteDataLoader


def convert_game(file):
    df = pd.read_csv(file)
    df = df.pivot('game_id', 'attr', 'val')
    df['players'] = df['player0']
    for i in range(1, 4):
        df['players'] += '|' + df['player' + str(i)].fillna('')

    df.drop(['player' + str(i) for i in range(5)], axis=1, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['game_id'] = df.index
    df = df[df['game_outcome'].notna()]

    return df[['game_id', 'game_outcome', 'players', 'ranked_status', 'timestamp']]


def main():
    api = RiotAPI(consts.API_KEY)
    hist = HistoryExtractor(summoner_names=consts.SUMMONER_NAMES, api=api)
    hist.extract(full_load=False)
    hist.load('data/game_records.csv')

    # Class for loading data into the site database
    loader = SiteDataLoader('../api/rest/db.sqlite3')

    if hist.new_data:
        # Game Identifier
        # games = pd.DataFrame({'game_id': hist.game_log['game_id'].unique()})
        # games['pk'] = games['game_id']
        # loader.upsert(src=games, dest='strife_game', pk='game_id')

        # Game - Player Relationship
        loader.query('SELECT * FROM strife_player')
        player_lkup = loader.result_set
        game_log = hist.game_log.join(player_lkup.set_index('player_name'), how='inner', on='player_name').\
            rename(columns={'id': 'player_id'}).\
            drop('player_name', axis=1)
        game_log['pk'] = game_log['game_id'].astype(str) + '_' + game_log['player_id'].astype(str)
        loader.upsert(src=game_log, dest='strife_gameplayerrelationship', pk='game_id || \'_\' || player_id')

        # Game Data
        game_records = pd.read_csv('data/game_records.csv')
        game_records['pk'] = game_records['game_id'].astype(str) + game_records['attr']
        loader.upsert(src=game_records, dest='strife_gameattribute', pk='game_id || attr')

        # GameWide Data
        game = convert_game('data/game_records.csv')
        game['pk'] = game['game_id']
        loader.upsert(src=game, dest='strife_game', pk='game_id')
    else:
        print('No new data to load.')

if __name__ == "__main__":
    main()