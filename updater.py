from haoshuupdater import HaoshuUrlUpdater
from ninefivexsupdater import NineFiveXSUpdater
from logger import Logger


class Updater:
    def __init__(self, urls):
        self.urls = urls
        self.updaters = []
        for url in urls.source_urls():
            if url.url_enable() is False:
                continue
            if url.url_class() == '365haoshu':
                self.updaters.append(HaoshuUrlUpdater(url))
            elif url.url_class() == '59xs':
                self.updaters.append(NineFiveXSUpdater(url))

    def start(self):
        for updater in self.updaters:
            updater.start()

    def wait(self):
        for updater in self.updaters:
            if updater.isAlive() is True:
                updater.join()

    def done(self):
        Logger.debug('All updater run over')
        for url in self.urls.source_urls():
            Logger.debug(url.url_location())
