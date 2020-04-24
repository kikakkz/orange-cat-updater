import redis
from config import RedisCfg
from logger import Logger


class RedisCli:
    instance_ = None

    def __init__(self, redis_desc):
        self.redis = RedisCfg(redis_desc)
        try:
            self.r = redis.Redis(host=self.redis.host(), port=self.redis.port())
        except Exception as e:
            Logger.error(e)

    @classmethod
    def instance(cls):
        return RedisCli.instance_

    @classmethod
    def initialize(cls, redis_desc):
        if RedisCli.instance_ is None:
            RedisCli.instance_ = RedisCli(redis_desc)

    @classmethod
    def finalize(cls):
        pass

    def set(self, key, val):
        self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)
