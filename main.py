__author__ = 'jchugh'
from kafka import KafkaClient


TEST_TOPIC = "test-topic"
ZOOKEEPER = "localhost:2181"
CONSUMER_GROUP = "test_group"
TOPIC_PARTITIONS = 5

KAFKA = KafkaClient("localhost:9092")
