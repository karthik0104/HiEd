"""
The central message handler class to handle all of the incoming messages from client.

The message can be of the following types: CONNECT, DISCONNECT, CHAT.
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

for i in range(1,1000000):
    p.set('foo1', 'Hey ! Whats up ? Long time, no see...How are you doing ? And how is life? All good ? Convey my best wishes to others as well !')
p.execute()
