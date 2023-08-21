# Apache Kafka-Spark Structured Streaming Via Docker Compose

The ideia is to write a system that processes real-time events sent by an application game server and,  on top of that, creates real-time data quality transformations and aggregations.

  ![image](https://github.com/brunohsilva88/kafka-spark-streaming/assets/91852282/2c923cb2-2f86-43f0-843b-be3dcf33419a)

It was used in this Pipeline:
 - Docker
 - Kafka Image (bitnami/kafka:latest)
 - Spark Image (apache/spark-py:latest)
 - WSL2 (Ubuntu 20.4)
 
Follow below step by step to run the pipeline:

1. GitHub Link https://github.com/brunohsilva88/kafka-spark-streaming.git. The struture has to be the same as image below:

  ![image](https://github.com/brunohsilva88/kafka-spark-streaming/assets/91852282/717e0f17-fe6f-4745-b369-1fd2884a6dd4)

2. Run command `docker compose up -d (or docker-compose up -d)"` (it'll depend of docker version)

3. Run command `docker exec -it kafka bash` to access the Kafka application

4. Run commands below to create topics:
    - `kafka-topics.sh --create --bootstrap-server 172.18.0.4:9092 --partitions 1 --replication-factor 1 --topic init`
    - `kafka-topics.sh --create --bootstrap-server 172.18.0.4:9092 --partitions 1 --replication-factor 1 --topic purchase`
    - `kafka-topics.sh --create --bootstrap-server 172.18.0.4:9092 --partitions 1 --replication-factor 1 --topic match`
  
5. In another terminal Run command `docker exec -it spark_master bash` to access the Spark application

6. Run command `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 main.py`

7. Back to kafka application and run the command `kafka-console-producer.sh --broker-list 172.18.0.4:9092 --topic init` to send events to topic Init. Follow below some examples:
   - {"platform":"Android","country":"BR","eventtype":"init","time":1691650216,"userid":1}
   - {"platform":"IOS","country":"US","eventtype":"init","time":1691650220,"userid":2}
   - {"platform":"IOS","country":"US","eventtype":"init","time":1691650220,"userid":4}
   - {"platform":"IOS","country":"US","eventtype":"init","time":1691650220,"userid":10}
   - {"platform":"IOS","country":"JP","eventtype":"init","time":1691650220,"userid":12}
   - {"platform":"Android","country":"BR","eventtype":"init","time":1691650216,"userid":7}
   - {"platform":"Android","country":"BR","eventtype":"init","time":1691650216,"userid":7}
   - {"platform":"Android","country":"BR","eventtype":"init","time":1691650216,"userid":55}
   - {"platform":"Android","country":"BR","eventtype":"init","time":1691650216,"userid":577}
  
8. Now back again to Spark Terminal and you'll be able to see the final data.
