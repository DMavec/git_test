from RiotAPI import RiotAPI
from ETLByName import ETLByName
import r_consts as Consts
import pickle

def main():
    api = RiotAPI('RGAPI-7de18e44-1325-4df9-b355-82dd7660d66b')
    name = 'menelaus34'
    for name in Consts.SUMMONER_NAMES:
        etl = ETLByName(name, api)
        etl.extract()

        #save_obj(etl, 'test_cache')
        #etl = load_obj('test_cache')

        etl.transform()

        etl.load(file_name='game_history.csv')

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    main()
