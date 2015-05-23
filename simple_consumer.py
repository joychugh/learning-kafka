__author__ = 'jchugh'
from main import TEST_TOPIC, KAFKA, CONSUMER_GROUP
from kafka import SimpleConsumer

kafka_consumer = SimpleConsumer(KAFKA, CONSUMER_GROUP, TEST_TOPIC,
                                auto_offset_reset='smallest')

for message in kafka_consumer:
    print(message)

