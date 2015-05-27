__author__ = 'jchugh'

from kafka import SimpleProducer
from main import CONFIG, KAFKA

def print_response(response):
    if response:
        print(response[0].error)
        print(response[0].offset)

producer = SimpleProducer(KAFKA)

producer_response = producer.send_messages(CONFIG.get('kafka', 'topic'),
                                           str('Hello World World Kafka Spark World Hello Kafka')
                                           .encode('utf-8'))
print_response(producer_response)

KAFKA.close()



