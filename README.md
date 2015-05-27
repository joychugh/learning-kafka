# learning-kafka
Just an attempt to learn kafka and its integration with Spark

#### How to run spark kafka integration directly from command line.

**`<SPARK-HOME>` refers to the directory where you extracted spark.**

1. Download http://search.maven.org/remotecontent?filepath=org/apache/spark/spark-streaming-kafka-assembly_2.10/1.3.1/spark-streaming-kafka-assembly_2.10-1.3.1.jar
2. Copy it to `<SPARK-HOME>/lib`
3. edit `<SPARK-HOME>/bin/compute_classpath.sh`
4. add the following line right before the last line (the print statement in the file)
  * `appendToClasspath "$FWDIR"/lib/spark-streaming-kafka-assembly_2.10-1.3.1.jar`
5. test that kafka assembly will get picked up by spark just run 
  * `<SPARK-HOME>/bin/compute_classpath.sh` 
  * it should look like (basically have the kafka assemly jar in the list)
    * `/usr/spark/conf:/usr/spark/lib/spark-assembly-1.3.1-hadoop2.6.0.jar:/usr/spark/lib/datanucleus-rdbms-3.2.9.jar:/usr/spark/lib/datanucleus-core-3.2.10.jar:/usr/spark/lib/datanucleus-api-jdo-3.2.6.jar:/usr/spark/lib/spark-streaming-kafka-assembly_2.10-1.3.1.jar`
	
5. to your ~/.bashrc append the following lines
  * `export SPARK_HOME=<SPARK-HOME>`
  * eg. `export SPARK_HOME=/usr/spark`
  * save and exit
  * NOTE: this wont work with an IDE, for an IDE you will have to manually add this env variable to run/debug options.

6. add `pyspark` module (`<SPARK-HOME>/python` to PYTHONPATH There are may ways to do it. I personally like this http://stackoverflow.com/a/12311321 
  * NOTE: pyspark code is not python3 compatible as of 1.3.1

You can just run your program straight from command line no need to reach out to spark-submit for your development code.
`python my_kafka_spark_example.py`
:)

