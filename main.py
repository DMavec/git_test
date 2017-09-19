from RiotAPI import RiotAPI
from ETLByName import ETLByName
from Visualise import Visualise
import constants as consts
import pandas as pd

def main():
    api = RiotAPI(consts.API_KEY)
    for name in consts.SUMMONER_NAMES:
        etl = ETLByName(name, api)
        etl.extract()
        etl.transform()
        etl.load('data/game_history.csv')

    game_history = pd.read_csv('data/game_history.csv')

    viz = Visualise(game_history, consts.SUMMONER_NAMES)
    viz.build()

if __name__ == "__main__":
    main()

## Data check - post-realising we were pulling non-matched games
# games = [api.get_match(game_id) for game_id in game_history['game_id'].unique()]
# game_type = [{'gameId': game['gameId'], 'gameMode': game['gameMode'], 'bans': len(game['teams'][0]['bans'])} for game in games]
# pd.DataFrame.from_dict(game_type).to_csv('data_check.csv', mode='w', index=False, encoding='utf-8')

## Caching script for dev purposes only
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