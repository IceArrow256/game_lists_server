from datetime import datetime as DT
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


def save_game_to_model(id: int):
    game = None
    release_date = None
    model.Game.create_table()
    db_games = model.Game.select().where(model.Game.id==id).objects()
    if len(db_games):
        db_game = db_games[0]
        if (DT.now() - db_game.date_last_updated).days > 30:
            game = giant_bomb.get_game(id).results
            if game['original_release_date']:
                release_date = DT.strptime(
                    game['original_release_date'], '%Y-%m-%d').date()
            db_game.date_last_updated = DT.now()
            db_game.name = game['name']
            db_game.image_url = game['image']['original_url']
            db_game.description = game['deck']
            db_game.release_date = release_date
            db_game.save()
    else:
        game = giant_bomb.get_game(id).results
        if game['original_release_date']:
            release_date = DT.strptime(
                game['original_release_date'], '%Y-%m-%d').date()
        db_game = model.Game.create(
            id=game['id'],
            date_last_updated=DT.now(),
            name=game['name'],
            image_url=game['image']['original_url'],
            description=game['deck'],
            release_date=release_date,
        )
    if game:
        if 'genres' in game and game['genres']:
            model.GameGenre.create_table()
            model.Genre.create_table()
            model.GameGenre.delete().where(model.GameGenre.game==db_game).execute()
            for genre in game['genres']:
                db_genres = model.Genre.select().where(model.Genre.id==genre['id']).objects()
                if len(db_genres):
                    db_genre = db_genres[0]
                    db_genre.name = genre['name']
                    db_genre.save()
                else:
                    db_genre = model.Genre.create(
                        id=genre['id'],
                        name=genre['name']
                    )
                model.GameGenre.create(
                    game=db_game,
                    genre=db_genre
                )
        if 'franchises' in game and game['franchises']:
            model.GameFranchise.create_table()
            model.Franchise.create_table()
            model.GameFranchise.delete().where(model.GameFranchise.game==db_game).execute()
            for franchise in game['franchises']:
                db_franchises = model.Franchise.select().where(model.Franchise.id==franchise['id']).objects()
                if len(db_franchises):
                    db_franchise = db_franchises[0]
                    db_franchise.name = franchise['name']
                    db_franchise.save()
                else:
                    db_franchise = model.Franchise.create(
                        id=franchise['id'],
                        name=franchise['name']
                    )
                model.GameFranchise.create(
                    game=db_game,
                    franchise=db_franchise
                )
        if 'platforms' in game and game['platforms']:
            model.GamePlatform.create_table()
            model.Platform.create_table()
            model.GamePlatform.delete().where(model.GamePlatform.game==db_game).execute()
            for platform in game['platforms']:
                db_platforms = model.Platform.select().where(model.Platform.id==platform['id']).objects()
                if len(db_platforms):
                    db_platform = db_platforms[0]
                    db_platform.name = platform['name']
                    db_platform.save()
                else:
                    db_platform = model.Platform.create(
                        id=platform['id'],
                        name=platform['name'],
                        abbreviation=platform['abbreviation']
                    )
                model.GamePlatform.create(
                    game=db_game,
                    platform=db_platform
                )
        if 'developers' in game and game['developers']:
            model.GameDeveloper.create_table()
            model.Developer.create_table()
            model.GameDeveloper.delete().where(model.GameDeveloper.game==db_game).execute()
            for developer in game['developers']:
                db_developers = model.Developer.select().where(model.Developer.id==developer['id']).objects()
                if len(db_developers):
                    db_developer = db_developers[0]
                    db_developer.name = developer['name']
                    if (DT.now() - db_developer.date_last_updated).days > 30:
                        company = giant_bomb.get_company(developer["id"]).results
                        db_developer.country = company['location_country']
                        db_developer.date_last_updated = DT.now()
                    db_developer.save()
                else:
                    company = giant_bomb.get_company(developer["id"]).results
                    db_developer = model.Developer.create(
                        id=developer['id'],
                        date_last_updated = DT.now(),
                        name=developer['name'],
                        country = company['location_country']
                    )
                model.GameDeveloper.create(
                    game=db_game,
                    developer=db_developer
                )
    return db_game.id


def generate_json_from_model(id: int):
    db_game = model.Game.select().where(model.Game.id==id).objects()[0]
    # franchises 
    db_franchises = model.Franchise.select().join(model.GameFranchise).where(model.GameFranchise.game==db_game).objects()
    franchises = []
    for franchise in db_franchises:
        franchises.append({
            'id': franchise.id,
            'name': franchise.name,
        })
    # genres 
    db_genres = model.Genre.select().join(model.GameGenre).where(model.GameGenre.game==db_game).objects()
    genres = []
    for genre in db_genres:
        genres.append({
            'id': genre.id,
            'name': genre.name,
        })
    # platforms 
    db_platforms = model.Platform.select().join(model.GamePlatform).where(model.GamePlatform.game==db_game).objects()
    platforms = []
    for platform in db_platforms:
        platforms.append({
            'id': platform.id,
            'name': platform.name,
            'abbreviation': platform.abbreviation,
        })
    # developer 
    db_developers = model.Developer.select().join(model.GameDeveloper).where(model.GameDeveloper.game==db_game).objects()
    developers = []
    for developer in db_developers:
        developers.append({
            'id': developer.id,
            'dateLastUpdated': developer.date_last_updated.replace(microsecond=0).isoformat(),
            'name': developer.name,
            'country': developer.country,
        })
    data =  {
        'id': db_game.id,
        'dateLastUpdated': db_game.date_last_updated.replace(microsecond=0).isoformat(),
        'name': db_game.name,
        'imageUrl': db_game.image_url,
        'description': db_game.description,
        'releaseDate': db_game.release_date.isoformat() if db_game.release_date else None,
        'developers': developers,
        'franchises': franchises,
        'genres': genres,
        'platforms': platforms,
    }
    return data
    
def search(name: str):
    ids = []
    model.Log.create_table()
    model.LogId.create_table()
    db_logs = model.Log.select().where(model.Log.name==name.lower()).objects()
    if len(db_logs) == 1:
        db_log = db_logs[0]
        if (DT.now() - db_log.date_last_updated).days > 30:
            model.LogId.delete().where(model.LogId.log==db_log).execute()
            for game in giant_bomb.search(name.lower(), 'game').results:
                ids.append(game['id'])
                model.LogId.create(
                    log = db_log,
                    game_id = game['id'],
                )
            db_log.date_last_updated = DT.now()
            db_log.save()
        else:
            db_log_ids = model.LogId.select().where(model.LogId.log==db_log).objects()
            for id in db_log_ids:
                ids.append(id.game_id)
    else:
        db_log = model.Log.create(name = name.lower(), date_last_updated = DT.now())
        for game in giant_bomb.search(name, 'game').results:
            ids.append(game['id'])
            model.LogId.create(
                log = db_log,
                game_id = game['id'],
            )
    return ids




class Game:
    def on_get(self, req, resp, guid):
        data = giant_bomb.get_game(guid).results
        resp.text = json.dumps(data)


class Games:
    def on_get(self, req, resp):
        name = req.params['name'] if 'name' in req.params else None
        data = []
        if name:
            for game_id in search(name):
                save_game_to_model(game_id)
                data.append(generate_json_from_model(game_id))
        else:
            data = {}
        resp.text = json.dumps(data)


class Search:
    def on_get(self, req, resp):
        pass
        # query = req.params['query'] if 'query' in req.params else None
        # data = giant_bomb.search(req.params['query'], 'game').results
        # model.Game.create_table()
        # for game in data:
        #     try:
        #         model.Game.insert(
        #             date_added=datetime.datetime.strptime(
        #                 game['date_added'], '%Y-%m-%d %H:%M:%S'),
        #             date_last_updated=datetime.datetime.strptime(
        #                 game['date_last_updated'], '%Y-%m-%d %H:%M:%S'),
        #             deck=game['deck'],
        #             guid=game['guid'],
        #             id=game['id'],
        #             image_url=game['image']['original_url'],
        #             name=game['name'],
        #             original_release_date=datetime.datetime.strptime(
        #                 game['original_release_date'], '%Y-%m-%d').date() if game['original_release_date'] else None,
        #         ).execute()
        #     except peewee.IntegrityError:
        #         pass
        # content = []
        # for game in model.Game.select().where(model.Game.name.contains(query)):
        #     content.append({
        #         'dateAdded': game.date_added.replace(microsecond=0).isoformat(),
        #         'dateLastUpdated': game.date_last_updated.replace(microsecond=0).isoformat(),
        #         'deck': game.deck,
        #         'guid': game.guid,
        #         'id': game.id,
        #         'imageUrl': game.image_url,
        #         'name': game.name,
        #         'originalReleaseDate': game.original_release_date.isoformat() if game.original_release_date else None,
        #     })
        #     resp.text = json.dumps(content)
        #     resp.status = falcon.HTTP_200
