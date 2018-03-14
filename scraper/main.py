import scraper.constants as consts
import pandas as pd
from scraper.HistoryExtractor import HistoryExtractor
from scraper.SiteDataTransformer import SiteDataTransformer

from scraper.RiotAPI import RiotAPI
from scraper.SiteDataLoader import SiteDataLoader


def main():
    # api = RiotAPI(consts.API_KEY)
    # hist = HistoryExtractor(summoner_names=consts.SUMMONER_NAMES, api=api)
    # hist.extract()
    # hist.load('scraper/data/game_records.csv')

    # transformer = SiteDataTransformer(game_history, consts.SUMMONER_NAMES)
    # transformer.build()

    site_data_loader = SiteDataLoader('site/db.sqlite3')

    game_log = pd.read_csv('scraper/data/game_log.csv')

    # Game Identifier
    games = pd.DataFrame({'game_id': game_log['game_id'].unique()})
    games['pk'] = games['game_id']
    site_data_loader.upsert(src=games, dest='stats_game', pk='game_id')

    # Game - Player Relationship
    site_data_loader.query('SELECT * FROM stats_player')
    player_lkup = site_data_loader.result_set
    game_log = game_log.join(player_lkup.set_index('player_name'), how='inner', on='player_name').\
        rename(columns={'id': 'player_id'}).\
        drop('player_name', axis=1)
    game_log['pk'] = game_log['game_id'].astype(str) + '_' + game_log['player_id'].astype(str)
    site_data_loader.upsert(src=game_log, dest='stats_gameplayerrelationship', pk='game_id || \'_\' || player_id')

    # Game Data
    # game_records = pd.read_csv('scraper/data/game_records.csv')
    # game_records['pk'] = game_records['game_id'].astype(str) + game_records['attr']
    # site_data_loader.upsert(src=game_records, dest='stats_gameattribute', pk='game_id || attr')


if __name__ == "__main__":
    main()

    # # Data check - post-realising we were pulling non-matched games
    # games = [api.get_match(game_id) for game_id in game_history['game_id'].unique()]
    # game_type = [{'gameId': game['gameId'],
    #               'gameMode': game['gameMode'],
    #               'bans': len(game['teams'][0]['bans'])}
    #              for game in games]
    # pd.DataFrame.from_dict(game_type).to_csv('data_check.csv', mode='w', index=False, encoding='utf-8')

    # Caching script for dev purposes only
    # import pickle
    # def save_obj(obj, name ):
    #     with open('obj/'+ name + '.pkl', 'wb') as f:
    #         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    #
    # def load_obj(name ):
    #     with open('obj/' + name + '.pkl', 'rb') as f:
    #         return pickle.load(f)
    #
    # save_obj(etl, 'test_cache')
    # etl = load_obj('test_cache')
