"""
The central message handler class to handle all of the incoming messages from client.

The message can be of the following types: CONNECT, DISCONNECT, CHAT, SAVE_DOC_DIFF, SAVE_DOC.
The corresponding action upon receiving a message could either sending it to RabbitMQ or Redis, depending on the usecase.
"""

def connectUser(sid):
    return None

def handleSocketMessage(message, sid):
    return None

def disconnectUser(sid):
    return None


'''
RabbitMQ Producer Configuration
'''
import pika

params = pika.URLParameters('amqps://annmvtxy:S_66rdXfWSJmjz9dQP3YyQ76LcVAPSSo@puffin.rmq2.cloudamqp.com/annmvtxy')
params._socket_timeout = 15

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='pdfprocess')

channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
print("[x] Message sent to consumer")

connection.close()

'''
Redis Python Client
'''
import redis

r = redis.Redis(
    host='redis-18779.c51.ap-southeast-2-1.ec2.cloud.redislabs.com',
    port=18779,
    password='h8cvH2HTS4BZkXXA6oqMVA5hUpexjZKC')

r.set('foo', 'bar')
value = r.get('foo')
print(value)

p = r.pipeline()

import time

for i in range(1,100):
    r.set('testk'+str(i), str(i) + 'Hey ! Whats up ? Long time, no see...How are you doing ? And how is life? All good ? Convey my best wishes to others as well !')

start_time = time.time()
p.execute()
end_time = time.time()
time_taken = end_time - start_time
print(time_taken)


from itertools import zip_longest

# iterate a list in batches of size n
def batcher(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)

for keybatch in batcher(r.scan_iter('testk*'), 10):
    print(keybatch)
    data = r.mget(*(tuple(_x for _x in keybatch if _x is not None)))

tuple(_x for _x in keybatch if _x is not None)

keys = r.keys('foo*')
data = r.mget(keys)


#################### Sorted Set Redis #################

message_list = ['Hey! Whats up ?', 'Nothing much. On your side?', 'Pretty Great', 'Cool !']

p = r.pipeline()

for i in range(0, len(message_list)):
    start_time = time.time()

    # 0 or 1 is to indicate the direction of the conversation
    p.zadd('karthik'+':'+'am4', {'[time:'+str(start_time) + '][0]' + message_list[i]: start_time})
    end_time = time.time()
    print(end_time - start_time)

start_time = time.time()
p.execute()
end_time = time.time()
print(end_time - start_time)

r.zadd('test_ssk2', {'All well !': 'karthik'+':'+'keerthi'+':'+time.time()})

r.zrange('test_ssk2', 0, 2, desc=False, withscores=True)
r.zscan('test_ssk2', match='P*')

a = r.zscan('karthik:am4')
b = a[1]

for c in b:
    print(c[0].decode('utf-8'))

trial = b[0][0].decode('utf-8')

import re
re.sub("\[time:.*\]", '', trial)
bool(re.search("\[time:.*\]", trial))

r.zrem('karthik:am4', '[time:1631276083.4704242]Nothing much. On your side?')

re.sub("\[time:[0-9]*\.[0-9]*\]", '', '[time:1631276083.4704242][patch]Nothing much. On your side?')

d = {'key1': ['value1', 'value2'], 'key2': ['value3', 'value4']}

l = {key: d[key] for key in d}



l = {v: key for key in d for v in d[key]}

from util.redis import RedisConnection
from config.argsparser import ArgumentsParser

configs = ArgumentsParser()

rc = RedisConnection(configs.redis_host, configs.redis_port, configs.redis_password)
r = rc.get_connection()

p = rc.get_pipeline(r)
rc.save_in_sorted_set_with_timestamp(p, 'document1', '@ok\n11123\nokthanks')
rc.execute_pipeline(p)