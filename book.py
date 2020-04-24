from logger import Logger


class Book:
    def __init__(self, book_id, source_host):
        self.native_id = book_id
        self.id = source_host.replace('.', '_') + book_id
        self.attrs = {}
        self.chapters = []

    def book_id(self):
        return self.id

    def book_native_id(self):
        return self.native_id

    def set_attr(self, attr, val):
        self.attrs[attr] = val

    def get_attr(self, attr):
        try:
            return self.attrs[attr]
        except Exception as e:
            Logger.error(e)
            self.dump()

    def dump(self):
        Logger.debug(self.id)
        for attr in self.attrs:
            Logger.debug('{} : {}' . format(attr, self.attrs[attr]))

    def add_chapter(self, chapter):
        self.chapters.append(chapter)
