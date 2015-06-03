__author__ = 'jchugh'
from kafka import KafkaClient
from config import config
from kafka import SimpleProducer

kafka_client = KafkaClient(config.get('kafka', 'hosts'))
producer = SimpleProducer(kafka_client, async=True)
