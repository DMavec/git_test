from r_api import RiotAPI
import r_consts as Consts

def main():
    api = RiotAPI('2f71320a-8bfd-4650-b391-b3ff56e06e0a')

    #api.update_static_summoner_ids()

    name = 'diggs'
    names_dict = eval(open('static_summoner_ids.txt', 'r').read())
    print names_dict
    summoner_dets = api.get_summoner_by_name(name)
    summoner_id = summoner_dets[name]['id']

    games = api.get_games(summoner_id)

    p_games = process_games(games, api, names_dict)
    print p_games

    f = open('games_history.CSV', 'w')
    for i in range(len(p_games)):
        for player in p_games[i]:
            f.write(str(i) + "," + player['summoner'] + "," + player['champion'] + "\n")



def process_games(games, api, names_dict):
    prc_games = []
    for game in games['games']:
        team = game['teamId']
        teammates = [x for x in game['fellowPlayers'] if x['teamId'] == team]

        prc_game = []
        for i in range(len(teammates)):
            tm_id = teammates[i]['summonerId']

            if tm_id in names_dict.keys():
                tm_name = names_dict[tm_id]
            else:
                tm_name = 'randycaek'

            tm_champ = api.static_get_champion(teammates[i]['championId'])['name']
            prc_game.append({'summoner': tm_name, 'champion': tm_champ})

        prc_games.append(prc_game)

    return prc_games

if __name__ == "__main__":
    main()
