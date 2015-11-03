URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{static}{region}/{url}',
    'summoner_by_name': 'v{version}/summoner/by-name/{names}',
    'game': 'v{version}/game/by-summoner/{id}/recent',
    'lol-static-data': 'v{version}/{end_url}'
}

API_VERSIONS = {
    'summoner': '1.4',
    'game': '1.3',
    'lol-static-data': '1.2'
}

REGIONS = {
    'oceania': 'oce'
}

SUMMONER_NAMES = [
    'diggs',
    'bumster',
    'mwaxy',
    'loui8sdstk',
    'smatties',
    '2dmin',
    'pangryanda',
    'menelaus34',
    'menelaus',
    'ridethellama',
    'dicedstk',
    'orangu',
    'shaarcer',
    'sellerie',
    'muncheroo',
    'splunkle',
    'endgame',
    'minisundae',
    'themrb',
    'panman',
    'saltimate',
    'thereisnosaurus',
    'kkfizzban'
]

NAMES_DICT = eval(open('static_summoner_ids.txt', 'r').read())