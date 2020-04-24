from logger import Logger


class Chapter:
    def __init__(self, cid, url, title, vip, index):
        self.url = url
        self.title = title
        self.vip = vip
        self.cid = cid
        self.index = index

    def chapter_url(self):
        return self.url

    def chapter_title(self):
        return self.title

    def chapter_vip(self):
        return self.vip

    def chapter_id(self):
        return self.cid

    def chapter_index(self):
        return self.index

    def dump(self):
        Logger.debug('Chapter {}/{}' .format(self.cid, self.title))
