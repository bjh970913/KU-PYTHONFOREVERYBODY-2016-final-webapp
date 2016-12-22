import os
from os.path import *
from tornado.ioloop import IOLoop
from tornado.web import Application, url, RequestHandler

from Note import Note

util = None
_note_dir_ = './notes'

class util:
    def list_notes(self, parent = _note_dir_):
        notes = []
        for file in os.listdir(parent):
            if isfile(join(parent, file)) and file[-5:]==".note":
                notes.append(file[:-5])
        return notes

    def get_note(self, title):
        return Note(title)

class main(RequestHandler):
    def get(self):
        notes = util.list_notes()
        self.render('templates/main.html', notes=notes)

class edit(RequestHandler):
    def get(self):
        title = self.get_query_arguments('title')
        if len(title) == 0:
            note = Note()
        else:
            note = util.get_note(title[0])

        self.render('templates/edit.html', note=note)
    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')

        note = Note(title)
        note.set_content(content)

        note.save()

        self.redirect('/')

class test(RequestHandler):
    def get(self):
        ldict = locals()
        fn = self.get_query_argument('fn')
        exec(fn, globals(), ldict)
        f = ldict['f']
        self.render_string(f.__repr__())

class view(RequestHandler):
    def get(self):
        title = self.get_query_arguments('title')
        if len(title) == 0:
            self.redirect('/')
            return
        else:
            note = util.get_note(title[0])
            print(note.title, note.content)
            self.render('templates/view.html', note=note)

if __name__ == '__main__':
    util = util()
    app = Application([
        url(r"/", main),
        url(r"/new", edit),
        url(r"/edit", edit),
        url(r"/view", view),
        url(r"/test", test)
    ])
    app.listen(8080)
    IOLoop.current().start()
