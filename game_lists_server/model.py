import peewee as P


class BaseModel(P.Model):
    class Meta:
        database = P.SqliteDatabase('game_lists_server.db')


class Game(BaseModel):
    guid = P.TextField()
    date_last_updated = P.DateTimeField()
    name = P.TextField()
    image_url = P.TextField()
    description = P.TextField()
    release_date = P.DateField(null=True)


class Developer(BaseModel):
    name = P.TextField()
    country = P.TextField()


class Franchise(BaseModel):
    name = P.TextField()


class Genre(BaseModel):
    name = P.TextField()


class Platform(BaseModel):
    name = P.TextField()
    abbreviation = P.TextField()


class GameDeveloper(BaseModel):
    game = P.ForeignKeyField(Game)
    developer = P.ForeignKeyField(Developer)


class GameFranchise(BaseModel):
    game = P.ForeignKeyField(Game)
    franchise = P.ForeignKeyField(Franchise)


class GameGenre(BaseModel):
    game = P.ForeignKeyField(Game)
    genre = P.ForeignKeyField(Genre)
