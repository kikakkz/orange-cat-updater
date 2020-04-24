from config import MysqlCfg
from logger import Logger
import pymysql
import threading


class MysqlCli:
    instance_ = None

    def __init__(self, mysql_desc):
        self.mysql = MysqlCfg(mysql_desc)
        try:
            self.db = pymysql.connect(self.mysql.host(), self.mysql.user(), self.mysql.password(), self.mysql.db())
        except Exception as e:
            Logger.error(e)
            raise e
        self.lock = threading.Lock()

    def finalize(self):
        self.db.close()

    @classmethod
    def initialize(cls, mysql_desc):
        if MysqlCli.instance_ is None:
            MysqlCli.instance_ = MysqlCli(mysql_desc)

    @classmethod
    def finalize(cls):
        if MysqlCli.instance_ is not None:
            MysqlCli.instance_.finalize()

    @classmethod
    def instance(cls):
        return MysqlCli.instance_

    def exec(self, sql):
        success = True
        result = None
        self.lock.acquire()
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            Logger.error(e)
            Logger.error(sql)
            success = False
        self.lock.release()
        return success, result

