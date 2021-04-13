import requests


class GiantBomb:
    def __init__(self, api_key):
        self._api_key = api_key

    def get_games(self):
        request = self._get('https://www.giantbomb.com/api/games/')
        return request.json()

    def search(self, query: str, resources):
        """
        resources:
          game
          franchise
          character
          concept
          object
          location
          person
          company
          video
        """
        request = self._get('https://www.giantbomb.com/api/search/',
                            filters={'query': query, 'resources': resources})
        return request.json()

    def _get(self, url: str, filters: dict = {}):
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'game_lists_server 0.0.1'
        request = requests.get(
            url, {'api_key': self._api_key, 'format': 'json'} | filters, headers=headers)
        print(request.url)
        print(request.headers)
        return request
