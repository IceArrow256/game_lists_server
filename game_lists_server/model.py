import peewee as P


class BaseModel(P.Model):
    class Meta:
        database = P.SqliteDatabase('game_lists_server.db')


class Game(BaseModel):
    id = P.AutoField()
    date_last_updated = P.DateTimeField()
    name = P.TextField()
    image_url = P.TextField()
    description = P.TextField(null=True)
    release_date = P.DateField(null=True)


class Developer(BaseModel):
    id = P.AutoField()
    date_last_updated = P.DateTimeField()
    name = P.TextField()
    country = P.TextField(null=True)


class Franchise(BaseModel):
    id = P.AutoField()
    name = P.TextField()


class Genre(BaseModel):
    id = P.AutoField()
    name = P.TextField()


class Platform(BaseModel):
    id = P.AutoField()
    name = P.TextField()
    abbreviation = P.TextField()

class Log(BaseModel):
    name = P.TextField(unique=True)
    date_last_updated = P.DateTimeField()

class LogId(BaseModel):
    log = P.ForeignKeyField(Log, on_delete='CASCADE')
    game_id = P.IntegerField()
    class Meta:
        primary_key = P.CompositeKey('log', 'game_id')

class GameDeveloper(BaseModel):
    game = P.ForeignKeyField(Game, on_delete='CASCADE')
    developer = P.ForeignKeyField(Developer, on_delete='CASCADE')
    class Meta:
        primary_key = P.CompositeKey('game', 'developer')


class GameFranchise(BaseModel):
    game = P.ForeignKeyField(Game, on_delete='CASCADE')
    franchise = P.ForeignKeyField(Franchise, on_delete='CASCADE')
    class Meta:
        primary_key = P.CompositeKey('game', 'franchise')


class GameGenre(BaseModel):
    game = P.ForeignKeyField(Game, on_delete='CASCADE')
    genre = P.ForeignKeyField(Genre, on_delete='CASCADE')
    class Meta:
        primary_key = P.CompositeKey('game', 'genre')

class GamePlatform(BaseModel):
    game = P.ForeignKeyField(Game, on_delete='CASCADE')
    platform = P.ForeignKeyField(Platform, on_delete='CASCADE')
    class Meta:
        primary_key = P.CompositeKey('game', 'platform')
