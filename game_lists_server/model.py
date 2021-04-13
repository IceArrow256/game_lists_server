import peewee as P


class BaseModel(P.Model):
    class Meta:
        database = P.SqliteDatabase('game_lists_server.db')


class Game(BaseModel):
    date_added = P.DateTimeField()
    date_last_updated = P.DateTimeField()
    deck = P.TextField()
    guid = P.TextField()
    image_url = P.TextField()
    name = P.TextField()
    original_release_date = P.DateField(null=True)


# class Developer(BaseModel):
#     pass


# class Franchise(BaseModel):
#     pass


# class Genre(BaseModel):
#     pass


# class Platform(BaseModel):
#     pass


# class Release(BaseModel):
#     pass


# Game.create_table()
# Game.create(id=444)
