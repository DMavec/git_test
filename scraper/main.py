import os
import pandas as pd
import constants as consts
from HistoryExtractor import HistoryExtractor
from RiotAPI import RiotAPI
from SiteDataLoader import SiteDataLoader


def convert_game_records(game_records):
    game = game_records.pivot('game_id', 'attr', 'val')
    game['players'] = game['player0']
    for i in range(1, 4):
        game['players'] += '|' + game['player' + str(i)].fillna('')

    game.drop(['player' + str(i) for i in range(5)], axis=1, inplace=True)
    game['timestamp'] = pd.to_datetime(game['timestamp'], unit='ms')
    game['game_id'] = game.index
    game = game[game['game_outcome'].notna()]
    game = game[['game_id', 'game_outcome', 'players', 'ranked_status', 'timestamp']]

    return game


def main():
    api = RiotAPI(consts.API_KEY)
    hist = HistoryExtractor(summoner_names=consts.SUMMONER_NAMES, api=api)
    hist.identify_new_games(full_load=F alse)
    hist.extract()
    hist.load('data/game_records.csv')

    # Class for loading data into the site database
    loader = SiteDataLoader('../api/rest/db.sqlite3')

    if hist.new_data:
        # Game - Player Relationship
        loader.query('SELECT * FROM strife_player')
        player_lkup = loader.result_set
        game_log = hist.game_log.join(player_lkup.set_index('player_name'), how='inner', on='player_name'). \
            rename(columns={'id': 'player_id'}). \
            drop('player_name', axis=1)
        game_log['pk'] = game_log['game_id'].astype(int).astype(str) + '_' + game_log['player_id'].astype(str)
        loader.upsert(src=game_log, dest='strife_gameplayerrelationship', pk='game_id || \'_\' || player_id')

        # Game Data
        game_records = pd.read_csv('data/game_records.csv')
        game_records['pk'] = game_records['game_id'].astype(str) + game_records['attr']
        loader.upsert(src=game_records, dest='strife_gameattribute', pk='game_id || attr')

        # GameWide Data
        game_records = pd.read_csv('data/game_records.csv')
        game = convert_game_records(game_records)
        game['pk'] = game['game_id']
        loader.upsert(src=game, dest='strife_game', pk='game_id')
    else:
        print('No new data to load.')


if __name__ == "__main__":
    if os.getcwd().endswith('riot_project'):
        os.chdir('scraper')

    main()
