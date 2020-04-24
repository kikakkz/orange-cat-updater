from config import Config
from urls import Urls
from updater import Updater
import time
import sys
from mysqlcli import MysqlCli
from rediscli import RedisCli
from dbhelper import DBHelper

if __name__ == "__main__":
    while True:
        config = Config('./updater-config.json')
        MysqlCli.initialize(config.mysql())
        RedisCli.initialize(config.redis())
        DBHelper.initialize()

        urls = Urls(config.urls())
        updater = Updater(urls)
        updater.start()
        updater.wait()
        updater.done()

        if config.one_shot() is True:
            sys.exit(0)

        time.sleep(config.interval())

        RedisCli.finalize()
        MysqlCli.finalize()
