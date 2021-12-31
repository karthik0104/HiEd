from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

class KafkaProducer:

    @classmethod
    def send_message(cls, message):
        producer.send('test', value=message)