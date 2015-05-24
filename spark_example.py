__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from main import TEST_TOPIC, ZOOKEEPER, CONSUMER_GROUP, TOPIC_PARTITIONS


sc = SparkContext("local[2]", "KafkaWordCount")
ssc = StreamingContext(sc, 1)
ksc = KafkaUtils.createStream(ssc, ZOOKEEPER, CONSUMER_GROUP, {TEST_TOPIC: TOPIC_PARTITIONS})

lines = ksc.map(lambda x: x[1])

words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()
ssc.start()
ssc.awaitTermination()

