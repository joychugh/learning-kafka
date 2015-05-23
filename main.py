__author__ = 'jchugh'
from kafka import KafkaClient


TEST_TOPIC = 'test-topic'
KAFKA = KafkaClient("localhost:9092")
