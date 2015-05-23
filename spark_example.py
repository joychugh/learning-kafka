__author__ = 'jchugh'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from main import TEST_TOPIC
from os import environ

environ["SPARK_HOME"] = "/usr/spark"
sc = SparkContext("local[2]", "KafkaWordCount")
ssc = StreamingContext(sc, 1)
ksc = KafkaUtils.createStream(ssc, "localhost:2181", "test_group", {TEST_TOPIC: 5})

#lines = ssc.socketTextStream("localhost", 9999)
lines = ksc.map(lambda x: x[1])
lines.pprint()

words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()
ssc.start()
ssc.awaitTermination()

