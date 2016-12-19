import time
import pickle
from os import sep


class Note:
    def __init__(self, title=""):
        super().__init__()
        self.base_path = "./notes"
        self.title = title

        if len(title)!=0:
            self.load()
        else:
            self.content = ''
            self.date = time.localtime()

    def set_basepath(self, path):
        self.base_path = path

    def set_title(self, title):
        self.title = title

    def set_date(self, date):
        self.date = date

    def set_content(self, content):
        self.content = content

    def load(self):
        if self.title == '':
            self.content = ''

        try:
            f = self.get_file()
            tmp_dict = pickle.load(f)
            f.close()

            self.__dict__.update(tmp_dict)
        except:
            self.save()
            pass

    def save(self):
        print('saving...', self.title, self.content)
        f = self.get_file(mode='wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def get_file(self, mode='rb'):
        if self.title == '':
            return None
        print('open', self.base_path + sep + self.title + ".note")
        return open(self.base_path + sep + self.title + ".note", mode)
