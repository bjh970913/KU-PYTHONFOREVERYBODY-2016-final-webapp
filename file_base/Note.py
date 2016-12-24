import os
import pickle
import time
from os import sep, path


class Note:
    def __init__(self):
        super().__init__()
        self.base_path = "./notes"
        self.title = None
        self.content = None
        self.date = time.localtime()
        self.ret = True

    def set_title(self, title):
        if self.title != title and self.title is not None:
            self.move(title)
        self.title = title

    def set_date(self, date):
        self.date = date

    def set_content(self, content):
        self.content = content

    def load(self):
        file = self.get_file()
        if file is None:
            self.ret = False
        else:
            try:
                tmp_dict = pickle.load(file)
                self.__dict__.update(tmp_dict)
                self.ret = True
            except:
                self.ret = False
            file.close()

        return self.ret

    def new(self):
        file = self.get_file(create=True, mode='wb')
        if not file or file is None:
            self.ret = False
        else:
            self.ret = True
            file.close()
        return self.ret

    def save(self):
        print('saving...', self.title, self.content)
        f = self.get_file(mode='wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def get_file(self, create=False, mode='rb'):
        file_name = self.base_path + sep + self.title + ".note"
        print('open', self.base_path + sep + self.title + ".note")
        if create and path.exists(file_name):
            return False

        try:
            return open(file_name, mode)
        except:
            return None

    def delete(self):
        file_name = self.base_path + sep + self.title + ".note"
        try:
            os.remove(file_name)
        except:
            pass

    def move(self, title):
        file_name_1 = self.base_path + sep + self.title + ".note"
        file_name_2 = self.base_path + sep + title + ".note"
        try:
            os.rename(file_name_1, file_name_2)
        except:
            pass
