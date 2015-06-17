__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext, dstream
from pyspark.streaming.kafka import KafkaUtils
from config import config
from simple_spark_example.utils import extract_hashtags
import simple_kafka
try:
    import simplejson as json
except ImportError:
    import json



def update_state(current_state, previous_state):
    return sum(current_state) + (previous_state or 0)


def filter_tweets(stream_to_filter):
    """
    Filters the topics, removing spam-spam like tweets
    :param stream_to_filter: the stream to apply the filter on
    :type stream_to_filter: dstream
    :return: dstream of filterd rdd's
    :rtype: dstream
    """
    filters = ('#JOBS', '#TWEETMYJOBS', '#HIRING')
    cleaned_dstream = stream_to_filter.transform(
        lambda rdd: rdd.filter(lambda e: e[0] not in filters)
    )
    return cleaned_dstream


def get_word_counts(streaming_context):
    """
    Returns the count of the words seen so far.
    :param streaming_context: the spark streaming context
    :return: dstream of word and its count tuple.
    :rtype: dstream
    """
    word_counts = streaming_context.map(lambda x: x[1]). \
        flatMap(lambda line: extract_hashtags(line)). \
        map(lambda word: (word, 1)). \
        updateStateByKey(update_state)
    return word_counts

def send_to_kafka(element):
    data = json.dumps(element)
    # http://apache-spark-user-list.1001560.n3.nabble.com/Writing-to-RabbitMQ-td11283.html
    simple_kafka.producer.send_messages(config.get('kafka', 'output_topic'), data.encode('utf-8'))

def send_dstream_data(dstream, max_items_to_send):
    max_items_to_send = max_items_to_send or 10
    dstream.foreachRDD(
        lambda rdd: send_to_kafka(rdd.sortBy(
            lambda v: v[1], False).collect()[:max_items_to_send+1]))

def start_spark(timeout=None, max_items_per_rdd_sent=None):
    sc = SparkContext("local[4]", "twitter.trending")
    ssc = StreamingContext(sc, 5)

    ssc.checkpoint('hdfs://localhost:9000/user/spark/checkpoint/')

    kafka_params = {
        'zookeeper.connect': config.get('zookeeper', 'host'),
        'group.id': config.get('kafka', 'group_id'),
        'metadata.broker.list': config.get('kafka', 'hosts')
    }

    ksc = KafkaUtils.createDirectStream(ssc,
                                        [config.get('kafka', 'topic')],
                                        kafka_params)

    hashtag_counts = get_word_counts(ksc)
    filtered_tweet_count = filter_tweets(hashtag_counts)
    send_dstream_data(filtered_tweet_count, max_items_per_rdd_sent)
    ssc.start()
    if timeout:
        ssc.awaitTermination(timeout)
        ssc.stop(stopSparkContext=True, stopGraceFully=True)
    else:
        ssc.awaitTermination()


if __name__ == '__main__':
    start_spark()
