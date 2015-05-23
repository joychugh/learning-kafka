__author__ = 'jchugh'
from main import TEST_TOPIC, KAFKA
from kafka import SimpleConsumer

kafka_consumer = SimpleConsumer(KAFKA, "test_group", TEST_TOPIC,
                                auto_offset_reset='smallest')

for message in kafka_consumer:
    print(message)

