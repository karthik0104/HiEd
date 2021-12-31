import redis
import time
from common import REDIS_POOL

class RedisConnection():

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    @classmethod
    def get_connection(cls):
        #r = redis.Redis(host=self.host, port=self.port, password=self.password)
        r = redis.StrictRedis(connection_pool=REDIS_POOL)
        return r

    @classmethod
    def get_pipeline(cls, r):
        p = r.pipeline()
        return p

    def save_in_sorted_set_with_timestamp(self, p, sorted_set_key, content, content_prefix=''):
        timestamp = time.time()
        p.zadd(sorted_set_key, {'[time:'+str(timestamp) + ']' + content_prefix + content: timestamp})

    def execute_pipeline(self, p):
        p.execute()
