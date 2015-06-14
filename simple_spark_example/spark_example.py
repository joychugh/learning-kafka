__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext, dstream
from pyspark.streaming.kafka import KafkaUtils
from config import config
from simple_spark_example.utils import extract_hashtags
import simple_kafka

def update_state(current_state, previous_state):
    return sum(current_state) + (previous_state or 0)

def get_word_counts(streaming_context):
    """
    Returns the count of the words seen so far.
    :param streaming_context:
    :return: dstream of word and its count tuple.
    :rtype: dstream
    """
    word_counts = streaming_context.map(lambda x: x[1]).\
        flatMap(lambda line: extract_hashtags(line)).\
        map(lambda word: (word, 1)).\
        updateStateByKey(update_state)
    return word_counts

def send_to_kafka(element):
    # http://apache-spark-user-list.1001560.n3.nabble.com/Writing-to-RabbitMQ-td11283.html
    simple_kafka.producer.send_messages(config.get('kafka', 'output_topic'), str(element).encode('utf-8'))

def send_dstream_data(dstream):
    dstream.foreachRDD(lambda rdd: send_to_kafka(rdd.collect()))

def start_spark(timeout):
    sc = SparkContext("local[4]", "KafkaWordCount")
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint('hdfs://localhost:9000/user/spark/checkpoint/')

    kafka_params = {
        'zookeeper.connect': config.get('zookeeper', 'host'),
        'group.id': config.get('kafka', 'group_id'),
        'metadata.broker.list': config.get('kafka', 'hosts')
    }

    ksc = KafkaUtils.createDirectStream(ssc,
                                        [config.get('kafka', 'topic')],
                                        kafka_params)

    word_count = get_word_counts(ksc)
    send_dstream_data(word_count)
    ssc.start()
    ssc.awaitTermination(timeout)
    ssc.stop(stopSparkContext=True, stopGraceFully=True)

if __name__ == '__main__':
    start_spark(60)
