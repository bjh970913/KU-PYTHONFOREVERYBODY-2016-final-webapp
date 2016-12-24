import os
from os.path import *

from tornado.ioloop import IOLoop
from tornado.web import Application, url, RequestHandler

from Note import Note

util = None
_note_dir_ = './notes'


class Util:
    def list_notes(self, parent=_note_dir_):
        notes = []
        for file in os.listdir(parent):
            if isfile(join(parent, file)) and file[-5:] == ".note":
                notes.append(file[:-5])
        return notes


class Main(RequestHandler):
    def get(self):
        notes = util.list_notes()
        self.render('templates/main.html', notes=notes)

    def post(self):
        pass


class Edit(RequestHandler):
    def get(self):
        title = self.get_query_argument('title')
        note = Note()
        note.set_title(title)
        if not note.load():
            self.redirect('/')
        self.render('templates/edit.html', note=note)

    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')

        note = Note()
        note.set_title(title)
        note.set_content(content)

        note.save()

        self.redirect('/')


class New(RequestHandler):
    def get(self):
        self.render('templates/new.html')

    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')

        note = Note()
        note.set_title(title)
        if not note.new():
            self.redirect('/')
            return
        note.set_content(content)

        note.save()

        self.redirect('/view?title=' + title)


class View(RequestHandler):
    def get(self):
        title = self.get_query_argument('title')

        note = Note()
        note.set_title(title)
        if not note.load():
            self.redirect('/')
        print(note.title, note.content)
        self.render('templates/view.html', note=note)

    def post(self):
        pass


if __name__ == '__main__':
    util = Util()
    app = Application([
        url(r"/", Main),
        url(r"/new", New),
        url(r"/edit", Edit),
        url(r"/view", View),
    ])
    app.listen(8080)
    IOLoop.current().start()
