import constants as consts
import pandas as pd
from HistoryExtractor import HistoryExtractor
from RiotAPI import RiotAPI
from SiteDataLoader import SiteDataLoader


def main():
    api = RiotAPI(consts.API_KEY)
    hist = HistoryExtractor(summoner_names=consts.SUMMONER_NAMES, api=api)
    hist.extract(full_load=False)
    hist.load('scraper/data/game_records.csv')

    # Class for loading data into the site database
    loader = SiteDataLoader('api/rest/db.sqlite3')

    # Game Identifier
    games = pd.DataFrame({'game_id': hist.game_log['game_id'].unique()})
    games['pk'] = games['game_id']
    loader.upsert(src=games, dest='strife_game', pk='game_id')

    # Game - Player Relationship
    loader.query('SELECT * FROM strife_player')
    player_lkup = loader.result_set
    game_log = hist.game_log.join(player_lkup.set_index('player_name'), how='inner', on='player_name').\
        rename(columns={'id': 'player_id'}).\
        drop('player_name', axis=1)
    game_log['pk'] = game_log['game_id'].astype(str) + '_' + game_log['player_id'].astype(str)
    loader.upsert(src=game_log, dest='strife_gameplayerrelationship', pk='game_id || \'_\' || player_id')

    # Game Data
    game_records = pd.read_csv('scraper/data/game_records.csv')
    game_records['pk'] = game_records['game_id'].astype(str) + game_records['attr']
    loader.upsert(src=game_records, dest='strife_gameattribute', pk='game_id || attr')


if __name__ == "__main__":
    main()
