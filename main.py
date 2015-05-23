__author__ = 'jchugh'
from kafka import KafkaClient


TEST_TOPIC = "test-topic"
SPARK_HOME = "/usr/spark"
ZOOKEEPER = "localhost:2181"
CONSUMER_GROUP = "test_group"

KAFKA = KafkaClient("localhost:9092")
