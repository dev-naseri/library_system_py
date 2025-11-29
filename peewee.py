import peewee
from peewee import SqliteDatabase

database = SqliteDatabase('data/test.db')

class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField(null=True)
    join_date = peewee.DateTimeField()


class Relationship(BaseModel):
    from_user = peewee.ForeignKeyField(User, backref='relationships')
    to_user = peewee.ForeignKeyField(User, backref='related_to')
    
    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )


class Message(BaseModel):
    user = peewee.ForeignKeyField(User, backref='messages')
    content = peewee.TextField()
    pub_date = peewee.DateTimeField()


def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])