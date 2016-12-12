import time
from os import pathsep
import pickle


class Note:
    def __init__(self, title=""):
        super().__init__()
        self.base_path = "."
        self.title = ""
        self.content = ""
        self.date = time.localtime()

        if title != "":
            f = self.get_file()
            self.__dict__.update(pickle.load(f))
            f.close()

    def set_basepath(self, path):
        self.base_path = path

    def set_title(self, title):
        self.title = title

    def set_date(self, date):
        self.date = date

    def set_content(self, content):
        self.content = content

    def save(self):
        f = self.get_file()
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def get_file(self):
        return open(self.base_path + pathsep + self.title + ".note", "wb")
