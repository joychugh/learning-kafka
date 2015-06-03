__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from config import config

from kafka import KafkaClient
from kafka import SimpleProducer


# This can be really run standalone, doesn't need to be inside this package.

sc = SparkContext("local[2]", "KafkaWordCount")
ssc = StreamingContext(sc, 10)
ssc.checkpoint('hdfs://localhost:9000/user/spark/checkpoint/')
ksc = KafkaUtils.createStream(ssc,
                              config.get('zookeeper', 'host'),
                              config.get('kafka', 'group_id'),
                              {config.get('kafka', 'topic'): config.getint('kafka', 'topic_partitions')},
                              )

def update_state(current_state, previous_state):
    return sum(current_state) + (previous_state or 0)

def send(element):
    # http://apache-spark-user-list.1001560.n3.nabble.com/Writing-to-RabbitMQ-td11283.html
    # TODO not to create each time, re-use the previously created object.
    kafka_client = KafkaClient(config.get('kafka', 'hosts'))
    producer = SimpleProducer(kafka_client, async=True)
    producer.send_messages(config.get('kafka', 'output_topic'), str(element).encode('utf-8'))

wordCounts = ksc.map(lambda x: x[1]).\
    flatMap(lambda line: line.split(" ")).\
    filter(lambda x: x.startswith('#')).\
    map(lambda word: (word, 1)).\
    updateStateByKey(update_state)
wordCounts.cache()
wordCounts.pprint(60)
wordCounts.foreachRDD(lambda rdd: rdd.foreach(send))
#wordCounts.saveAsTextFiles('hdfs://localhost:9000/user/spark/wordcount')
ssc.start()
ssc.awaitTermination()

