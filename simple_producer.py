__author__ = 'jchugh'

from datetime import date, datetime
from kafka import SimpleProducer
from main import TEST_TOPIC, KAFKA

def print_response(response):
    if response:
        print(response[0].error)
        print(response[0].offset)

producer = SimpleProducer(KAFKA)

producer_response = producer.send_messages(TEST_TOPIC, str(date.today()).encode('utf-8'))
print_response(producer_response)
producer_response = producer.send_messages(TEST_TOPIC, str(datetime.now().second).encode('utf-8'))
print_response(producer_response)

KAFKA.close()



