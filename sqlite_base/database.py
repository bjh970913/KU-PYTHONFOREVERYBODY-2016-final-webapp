from datetime import datetime

from peewee import *

db = SqliteDatabase('note.db')


class Note(Model):
    id = PrimaryKeyField()
    title = CharField()
    content = TextField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)

    def __repr__(self):
        return "<Note: ({i}) title='{t}' content='{c}'>".format(i=self.id, t=self.title, c=self.content)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Note])
