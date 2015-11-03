import requests
import RiotAPI_constants as Consts

class RiotAPI(object):
    def __init__(self, api_key, region=Consts.REGIONS['oceania']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, static=False, params={}):
        # Put additional parameters into args
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            Consts.URL['base'].format(
                proxy='global' if static else self.region,
                static='static-data/' if static else '',
                region=self.region,
                url=api_url
            ),
            params=args
        )

        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_games(self, id):
        api_url = Consts.URL['game'].format(
            version=Consts.API_VERSIONS['game'],
            id=id
        )
        return self._request(api_url)


    def update_static_summoner_ids(self):
        ids = {}
        for name in Consts.SUMMONER_NAMES:
            print 'Retrieving =>',name
            try:
                id = self.get_summoner_by_name(name)[name]['id']
                ids[id] = name
            except:
                print 'WARNING: Name not found.'

        target = open('static_summoner_ids.txt', 'w')
        target.write(str(ids))

    # lol-static-data-v1.2
    def _static_request(self, end_url):
        return self._request(
            Consts.URL['lol-static-data'].format(
                version=Consts.API_VERSIONS['lol-static-data'],
                end_url=end_url
            ),
            static=True
        )

    def static_get_champion_id(self, champ_id):
        return self._static_request(
            'champion/{id}'.format(id=champ_id),
        )

    def static_get_champion(self):
        return self._static_request(
            'champion/',
        )