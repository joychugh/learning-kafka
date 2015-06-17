__author__ = 'jchugh'
from config import config
from kafka import KafkaConsumer


kafka_consumer = KafkaConsumer(bootstrap_servers=[config.get('kafka', 'hosts')],
                               client_id=config.get('kafka', 'client_id'),
                               group_id=config.get('kafka', 'group_id'),
                               auto_commit_enable=config.getboolean('kafka', 'auto_commit'),
                               auto_offset_reset=config.get('kafka', 'auto_offset_reset'),
                               deserializer_class=lambda msg: msg.decode('utf-8'),
                               auto_commit_interval_ms=config.getint('kafka', 'auto_commit_time_ms'))

kafka_consumer.set_topic_partitions(config.get('kafka', 'output_topic'))


while True:
    data = kafka_consumer.next()
    print data.value

