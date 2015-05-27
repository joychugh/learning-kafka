__author__ = 'jchugh'
from main import KAFKA, CONFIG
from kafka import SimpleConsumer

kafka_consumer = SimpleConsumer(KAFKA,
                                CONFIG.get('kafka', 'consumer_group'),
                                CONFIG.get('kafka', 'topic'),
                                auto_offset_reset=CONFIG.get('kafka', 'auto_offset_reset'))

for message in kafka_consumer:
    print(message)

