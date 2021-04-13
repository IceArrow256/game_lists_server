import datetime
import json
import os

import dotenv
import falcon
import falcon.http_error
import peewee

import game_lists_server.model as model
from game_lists_server.giant_bomb import GiantBomb

dotenv.load_dotenv()

giant_bomb = GiantBomb(os.getenv('API_KEY'))


class Search:
    def on_get(self, req, resp):
        query = req.params['query']
        if 'query' in req.params:
            data = giant_bomb.search(req.params['query'], 'game')
            model.Game.create_table()
            if 'results' in data:
                for game in data['results']:
                    try:
                        model.Game.insert(
                            date_added=datetime.datetime.strptime(
                                game['date_added'], '%Y-%m-%d %H:%M:%S'),
                            date_last_updated=datetime.datetime.strptime(
                                game['date_last_updated'], '%Y-%m-%d %H:%M:%S'),
                            deck=game['deck'],
                            guid=game['guid'],
                            id=game['id'],
                            image_url=game['image']['original_url'],
                            name=game['name'],
                            original_release_date=datetime.datetime.strptime(
                                game['original_release_date'], '%Y-%m-%d').date() if game['original_release_date'] else None,
                        ).execute()
                    except peewee.IntegrityError:
                        pass
            content = []
            for game in model.Game.select().where(model.Game.name.contains(query)):
                content.append({
                    'dateAdded': game.date_added.replace(microsecond=0).isoformat(),
                    'dateLastUpdated': game.date_last_updated.replace(microsecond=0).isoformat(),
                    'deck': game.deck,
                    'guid': game.guid,
                    'id': game.id,
                    'imageUrl': game.image_url,
                    'name': game.name,
                    'originalReleaseDate': game.original_release_date.isoformat() if game.original_release_date else None,
                })
            resp.text = json.dumps(content)
            resp.status = falcon.HTTP_200
