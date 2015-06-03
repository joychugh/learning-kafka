__author__ = 'jchugh'
from config import config
from kafka import KafkaConsumer


kafka_consumer = KafkaConsumer(bootstrap_servers=[config.get('kafka', 'hosts')],
                               client_id=config.get('kafka', 'client_id'),
                               group_id=config.get('kafka', 'group_id'),
                               auto_commit_enable=True,
                               auto_offset_reset=config.get('kafka', 'auto_offset_reset'),
                               deserializer_class=lambda msg: msg)

kafka_consumer.set_topic_partitions(config.get('kafka', 'topic'))


while True:
    data = kafka_consumer.next()
    print data.value

