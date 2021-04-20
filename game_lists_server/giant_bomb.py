import requests


class Responses:
    def __init__(self, data: dict):
        self.status_code = data['status_code']
        self.error = data['error']
        self.number_of_total_results = data['number_of_total_results']
        self.number_of_page_results = data['number_of_page_results']
        self.limit = data['limit']
        self.offset = data['offset']
        self.results = data['results']


class GiantBomb:
    def __init__(self, api_key):
        self._api_key = api_key

    def get_company(self, id: int):
        """
        Keyword arguments:
        guid -- for use in single item api call for company
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/company/3010-{id}/').json())

    def get_companies(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/companies/').json())

    def get_franchise(self, guid):
        """
        Keyword arguments:
        guid -- for use in single item api call for franchise
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/franchise/{guid}/').json())

    def get_franchises(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/game/').json())

    def get_game(self, id):
        """
        Keyword arguments:
        guid -- for use in single item api call for game
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/game/3030-{id}/').json())

    def get_games(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/games/').json())

    def get_game_rating(self, guid):
        """
        Keyword arguments:
        guid -- for use in single item api call for game_rating
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/genre/{guid}/').json())

    def get_game_ratings(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/genres/').json())

    def get_genre(self, guid):
        """
        Keyword arguments:
        guid -- for use in single item api call for genre
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/genre/{guid}/').json())

    def get_genres(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/genres/').json())

    def get_platform(self, guid):
        """
        Keyword arguments:
        guid -- for use in single item api call for platform
        """
        return Responses(self._get(f'hhttps://www.giantbomb.com/api/platform/{guid}/').json())

    def get_platforms(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/platforms/').json())

    def get_release(self, guid):
        """
        Keyword arguments:
        guid -- for use in single item api call for release
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/release/{guid}/').json())

    def get_releases(self):
        """
        Keyword arguments:
        """
        return Responses(self._get(f'https://www.giantbomb.com/api/releases/').json())

    def search(self, query: str, resources):
        """
        resources -- list of resources to filter results. This filter can accept multiple arguments, each delimited with a ",". Available options: ["game", "franchise", "character", "concept", "object", "location", "person", "company", "video"]
        """
        return Responses(self._get('https://www.giantbomb.com/api/search/', filters={'query': query, 'resources': resources}).json())

    def _get(self, url: str, filters: dict = {}):
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'game_lists_server 0.0.1'
        request = requests.get(
            url, {'api_key': self._api_key, 'format': 'json'} | filters, headers=headers)
        print(request.url)
        print(request.headers)
        return request
