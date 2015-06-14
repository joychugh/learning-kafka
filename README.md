# learning-kafka
Just an attempt to learn kafka and its integration with Spark

### Installation Notes

Python libraries required
* [kafka-python](https://github.com/mumrah/kafka-python) *version 0.9.4-dev used for this project*
* [requests](https://pypi.python.org/pypi/requests/2.7.0)
* [uritools](https://pypi.python.org/pypi/uritools/0.12.0)
* pyspark comes bundled with spark.
* *optional* [simplejson](https://pypi.python.org/pypi/simplejson/3.7.2)

#### How to run spark kafka integration directly from PyCharm.
**`<SPARK-HOME>` refers to the directory where you extracted spark.**

1. Download http://search.maven.org/remotecontent?filepath=org/apache/spark/spark-streaming-kafka-assembly_2.10/1.4.0/spark-streaming-kafka-assembly_2.10-1.4.0.jar
2. Copy it to `<SPARK-HOME>/lib`
3. edit `<SPARK-HOME>/conf/spark-defaults.conf` (if doesn't exist, create file or rename `spark-defaults.conf.template` to `spark-defaults.conf` in the same directory) 
4. add the following line to the end of the
  * `spark.driver.extraClassPath      <SPARK-HOME>/lib/spark-streaming-kafka-assembly_2.10-1.4.0.jar`
  * eg. `spark.driver.extraClassPath      /usr/spark/lib/spark-streaming-kafka-assembly_2.10-1.4.0.jar`

5. to your ~/.bashrc append the following lines
  * `export SPARK_HOME=<SPARK-HOME>`
  * eg. `export SPARK_HOME=/usr/spark`
  * save and exit
  * OR in your IDE add this to your runtime environment variables
  * OR when you create spark-context pass this path as an argument.

6. add `pyspark` module (`<SPARK-HOME>/python` to PYTHONPATH There are may ways to do it. I personally like this http://stackoverflow.com/a/12311321

You can just run your program straight from command line no need to reach out to spark-submit for your development code.
`python my_kafka_spark_example.py`
:)

