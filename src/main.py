from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,LongType,IntegerType,FloatType,StringType,TimestampType,LongType
from pyspark.sql.functions import *

# Created the schema for Init Events
initSchema = StructType([
                StructField("platform",StringType(),False),
                StructField("country",StringType(),False),
                StructField("eventtype",StringType(),False),
                StructField("time",TimestampType(),False),
                StructField("userid",LongType(),False)
            ])

# Created the schema for Match Events
matchSchema = StructType() \
      .add("user_a_postmatch_info",StructType() \
        .add("coin_balance_after_match", IntegerType())
        .add("level_after_match", IntegerType())
        .add("device", StringType())
        .add("platform", StringType())
        ) \
      .add("user_b_postmatch_info",StructType() \
        .add("coin_balance_after_match", IntegerType())
        .add("level_after_match", IntegerType())
        .add("device", StringType())
        .add("platform", StringType())
        ) \
      .add("time", TimestampType()) \
      .add("user_a", StringType()) \
      .add("user_b", StringType()) \
      .add("winner",StringType()) \
      .add("game_tier", IntegerType()) \
      .add("duration",IntegerType())

# Created the schema for Purchase Events
purchaseSchema = StructType([
                StructField("productid",LongType(),False),
                StructField("purchasevalue",FloatType(),False),
                StructField("eventtype",StringType(),False),
                StructField("time",TimestampType(),False),
                StructField("userid",LongType(),False)
            ])

# Created the spark session
spark = SparkSession \
    .builder \
    .appName("kafka_main") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Starting reading data from Kafka (each Event)
df_init = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "172.18.0.4:9092") \
  .option("subscribe", "init") \
  .option("delimeter",",") \
  .option("startingOffsets", "earliest") \
  .load()

df_match = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "172.18.0.4:9092") \
  .option("subscribe", "match") \
  .option("delimeter",",") \
  .option("startingOffsets", "earliest") \
  .load()

df_purchase = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "172.18.0.4:9092") \
  .option("subscribe", "purchase") \
  .option("delimeter",",") \
  .option("startingOffsets", "earliest") \
  .load()

# Selecting only the values from Json
df_dataInit = df_init.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),initSchema).alias("dataInit")).select("dataInit.*")
df_dataMatch = df_match.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),matchSchema).alias("dataMatch")).select("dataMatch.*")
df_dataPurchase = df_purchase.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),purchaseSchema).alias("dataMatch")).select("dataMatch.*")

# Showing the Schema
df_dataInit.printSchema()
df_dataMatch.printSchema()
df_dataPurchase.printSchema()

# Aggregating data by Day, Country and Plataform to get the number of distinct access
dfUsersAccess = df_dataInit.groupBy(dayofmonth("time").alias("day"),"country", "platform").agg(approx_count_distinct('userid').alias('qtAccess'))

# Wrinting (Showing) aggregated data in console
dfUsersAccess.writeStream \
  .outputMode("complete") \
  .format("console") \
  .start() \
  .awaitTermination()
