import redis
import time

class RedisConnection():

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def get_connection(self):
        r = redis.Redis(host=self.host, port=self.port, password=self.password)
        return r

    def get_pipeline(self, r):
        p = r.pipeline()
        return p

    def save_in_sorted_set_with_timestamp(self, p, sorted_set_key, content, content_prefix=''):
        timestamp = time.time()
        p.zadd(sorted_set_key, {'[time:'+str(timestamp) + ']' + content_prefix + content: timestamp})

    def execute_pipeline(self, p):
        p.execute()
