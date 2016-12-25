from tornado.ioloop import IOLoop
from tornado.web import Application, url, RequestHandler

from sqlite_base.database import *


class Main(RequestHandler):
    def get(self):
        alert = self.get_query_argument('alert', default='')
        sort = self.get_query_argument('sort', default='id_dsc')

        o = sort[:-4]
        if o == 'id':
            o = Note.id
        elif o == 'title':
            o = Note.title
        elif o == 'created':
            o = Note.created
        elif o == 'updated':
            o = Note.updated
        else:
            o = Note.id

        v = sort[-4:]
        if v == '_asc':
            o = o.asc()
        else:
            o = o.desc()

        notes = []
        for i in Note.select().order_by(o):
            notes.append(i)

        self.render('templates/list.html', notes=notes, alert=alert)

    def post(self):
        pass


class New(RequestHandler):
    def get(self):
        self.render('templates/new.html')

    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')

        note = Note(title=title, content=content)
        note.save()

        self.redirect('/view?id=' + str(note.id))


class Edit(RequestHandler):
    def get(self):
        try:
            id = self.get_query_argument('id')

            note = Note.select().where(Note.id == id).get()

            self.render('templates/edit.html', note=note)
            return
        except:
            self.redirect('/?alert=Note does not exist')

    def post(self):
        try:
            id = self.get_body_argument('id')
            title = self.get_body_argument('title')
            content = self.get_body_argument('content')

            note = Note.select().where(Note.id == id).get()
            note.title = title
            note.content = content
            note.updated = datetime.now()
            note.save()

            self.redirect('/view?id=' + str(note.id))
            return
        except:
            self.redirect('/?alert=Note does not exist')


class View(RequestHandler):
    def get(self):
        try:
            id = self.get_query_argument('id')
            note = Note.select().where(Note.id == id).get()
            self.render('templates/view.html', note=note)
            return
        except:
            self.redirect('/?alert=Note does not exist')

    def post(self):
        pass


class Delete(RequestHandler):
    def get(self):
        try:
            id = self.get_query_argument('id')
            note = Note.select().where(Note.id == id).get()
            note.delete_instance()
            self.redirect('/?alert=Successfully deleted.')
            return
        except:
            self.redirect('/?alert=Note does not exist')

    def post(self):
        pass


if __name__ == '__main__':
    db.connect()
    app = Application([
        url(r"/", Main),
        url(r"/new", New),
        url(r"/edit", Edit),
        url(r"/view", View),
        url(r"/delete", Delete)
    ])
    app.listen(8080)
    IOLoop.current().start()
