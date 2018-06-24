import pandas as pd
from SiteDataLoader import SiteDataLoader

# Class for loading data into the site database
loader = SiteDataLoader('../api/rest/db.sqlite3')

def convert_game(file):
    df = pd.read_csv(file)
    df = df.pivot('game_id', 'attr', 'val')
    df['players'] = df['player0']
    for i in range(1, 4):
        df['players'] += '|' + df['player' + str(i)].fillna('')

    df.drop(['player' + str(i) for i in range(5)], axis=1, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df[['game_outcome','players','ranked_status','timestamp']]

# GameWide Data
gamestats = convert_game('data/game_records.csv')
print(gamestats)
gamestats.to_csv('data/game_stats.csv')
# loader.upsert(src=gamestats, dest='strife_game', pk='game_id')
