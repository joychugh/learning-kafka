__author__ = 'jchugh'
from kafka import KafkaClient
import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read("configurations.ini")
TEST_TOPIC = "test-topic"
ZOOKEEPER = "localhost:2181"
CONSUMER_GROUP = "test_group"
TOPIC_PARTITIONS = 5

KAFKA = KafkaClient('{host}:{port}'.format(
    host=CONFIG.get('kafka', 'host'),
    port=CONFIG.get('kafka', 'port')
    )
)
