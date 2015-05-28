__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from main import CONFIG


sc = SparkContext("local[2]", "KafkaWordCount")
ssc = StreamingContext(sc, 1)
ksc = KafkaUtils.createStream(ssc,
                              CONFIG.get('zookeeper', 'host'),
                              CONFIG.get('kafka', 'consumer_group'),
                              {CONFIG.get('kafka', 'topic'): CONFIG.get('kafka', 'topic_partitions')}
                              )

lines = ksc.map(lambda x: x[1])

words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()
ssc.start()
ssc.awaitTermination()

