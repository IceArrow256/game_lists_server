import datetime
import json
import mimetypes
import os

import dotenv
import falcon
import falcon.http_error
import peewee

import game_lists_server.model as model
from game_lists_server.giant_bomb import GiantBomb

dotenv.load_dotenv()

giant_bomb = GiantBomb(os.getenv('API_KEY'))


def save_game_to_model(guid: str):
    # basic
    guid = guid
    date_last_updated = datetime.datetime.now()
    # game
    giant_bomb_game = giant_bomb.get_game(guid).results
    id = giant_bomb_game['id']
    name = giant_bomb_game['name']
    image_url = giant_bomb_game['image']['original_url']
    description = giant_bomb_game['deck']
    release_date = datetime.datetime.strptime(giant_bomb_game['original_release_date'], '%Y-%m-%d').date() if giant_bomb_game['original_release_date'] else None
    # genres 
    genres = []
    if 'genres' in giant_bomb_game:
        for genre in giant_bomb_game['genres']:
            genres.append({
                'id': genre['id'],
                'name': genre['name'],
            })
    # franchises 
    franchises = []
    for franchise in giant_bomb_game['franchises']:
        franchises.append({
            'id': franchise['id'],
            'name': franchise['name'],
        })
    # platforms 
    platforms = []
    for platform in giant_bomb_game['platforms']:
        platforms.append({
            'id': platform['id'],
            'name': platform['name'],
            'abbreviation': platform['abbreviation'],
        })
    # developer 
    developers = []
    for developer in giant_bomb_game['developers']:
        giant_bomb_developer = giant_bomb.get_company(f'3010-{developer["id"]}').results
        developers.append({
            'id': giant_bomb_developer['id'],
            'name': giant_bomb_developer['name'],
            'country': giant_bomb_developer['location_country'],
        })
        
    # output
    data =  {
        'id': id,
        'guid': guid,
        'dateLastUpdated': date_last_updated.replace(microsecond=0).isoformat(),
        'name': name,
        'imageUrl': image_url,
        'description': description,
        'releaseDate': release_date.isoformat() if release_date else None,
        'platforms': platforms,
        'developers': developers,
        'genres': genres,
    }
    return data

def generate_json_from_model():
    pass

class Game:
    def on_get(self, req, resp, guid):
        data = giant_bomb.get_game(guid).results
        resp.text = json.dumps(data)


class Games:
    def on_get(self, req, resp):
        name = req.params['name'] if 'name' in req.params else None
        data = []
        if name:
            for game in giant_bomb.search(name, 'game').results:
                data.append(save_game_to_model(game['guid']))
        else:
            data = {'fuck': 'you'}
        resp.text = json.dumps(data)


class Search:
    def on_get(self, req, resp):
        query = req.params['query'] if 'query' in req.params else None
        data = giant_bomb.search(req.params['query'], 'game').results
        model.Game.create_table()
        for game in data:
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
