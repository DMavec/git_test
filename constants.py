import pandas as pd

API_KEY = pd.read_csv('data/api_key.txt')

URL = {
    'base': 'https://{proxy}.api.riotgames.com/lol/{static}{url}',
    'summoner_by_name': 'summoner/v{version}/summoners/by-name/{names}',
    'game': 'v{version}/game/by-summoner/{id}/recent',
    'lol-static-data': 'v{version}/{end_url}',
    'match-recent': 'match/v{version}/matchlists/by-account/{id}/recent',
    'match': 'match/v{version}/matches/{id}'
}


API_VERSIONS = {
    'summoner': '3',
    'game': '1.3',
    'match': '3',
    'lol-static-data': '3'
}

REGIONS = {
    'oceania': 'oc1'
}

SUMMONER_NAMES = [
    'diggs',
    'bumster',
    'mwaxy',
    'loui8sdstk',
    'smatties',
    #'2dmin',
    'skandaras',
    #'pangryanda',
    'menelaus34',
    #'menelaus',
    #'ridethellama',
    'dicedstk',
    #'orangu',
    #'shaarcer',
    #'sellerie',
    #'muncheroo',
    #'splunkle',
    'endgamedos',
	'loui9sdstk'
    #'minisundae',
    #'themrb',
    #'panman',
    #'saltimate',
    #'thereisnosaurus',
    #'kkfizzban'
]

OLD_IDS = pd.read_csv('data/load_log.csv')