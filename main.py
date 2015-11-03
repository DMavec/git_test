from RiotAPI_object import RiotAPI
import RiotAPI_constants as Consts

def main():
    api = RiotAPI('2f71320a-8bfd-4650-b391-b3ff56e06e0a')

    #api.update_static_summoner_ids()

    #name = 'diggs'
    #p_games = process_games(name, api)
    #print p_games
    #output_game(p_games)
    champ_list = [value['name'] for attribute, value in api.static_get_champion()['data'].iteritems()]
    champ_list.sort()
    print champ_list

def process_games(name, api):
    summoner_dets = api.get_summoner_by_name(name)
    summoner_id = summoner_dets[name]['id']

    games = api.get_games(summoner_id)

    prc_games = []
    for game in games['games']:
        team = game['teamId']
        teammates = [x for x in game['fellowPlayers'] if x['teamId'] == team]
        champ_name = api.static_get_champion_id(game['championId'])['name']

        prc_game = [{'summoner': name, 'champion': champ_name}]
        for i in range(len(teammates)):
            print teammates[i]
            tm_id = teammates[i]['summonerId']

            if tm_id in Consts.NAMES_DICT.keys():
                tm_name = Consts.NAMES_DICT[tm_id]
            else:
                tm_name = 'randycaek'

            tm_champ = api.static_get_champion_id(teammates[i]['championId'])['name']
            print(str(i) + " " + tm_name + " " + tm_champ)
            prc_game.append({'summoner': tm_name, 'champion': tm_champ})

        prc_games.append(prc_game)

    return prc_games

def output_game(p_games):
    f = open('games_history.CSV', 'w')
    f.write('game_id,summoner_name,champion\n')
    for i in range(len(p_games)):
        for player in p_games[i]:
            f.write(str(i) + "," + player['summoner'] + "," + player['champion'] + "\n")

if __name__ == "__main__":
    main()
