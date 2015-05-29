__author__ = 'jchugh'
from main import CONFIG
from kafka import KafkaConsumer


kafka_consumer = KafkaConsumer(bootstrap_servers=[CONFIG.get('kafka', 'hosts')],
                               client_id=CONFIG.get('kafka', 'client_id'),
                               group_id=CONFIG.get('kafka', 'group_id'),
                               auto_commit_enable=True,
                               auto_offset_reset=CONFIG.get('kafka', 'auto_offset_reset'),
                               deserializer_class=lambda msg: msg)

kafka_consumer.set_topic_partitions(CONFIG.get('kafka', 'topic'))


while True:
    print kafka_consumer.next()

