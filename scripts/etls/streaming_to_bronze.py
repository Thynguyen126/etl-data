from pyspark.sql import SparkSession

scala_version = '2.12'
spark_version = '3.3.0'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.3'
]
spark = SparkSession.builder \
   .appName("streaming_to_bronze") \
   .config("spark.driver.host", "localhost") \
   .config("spark.jars.packages", ",".join(packages)) \
   .getOrCreate()

# Create DataFrame representing the stream of input lines from kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9093") \
  .option("subscribe", "orders") \
  .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Split the lines into words
# words = df.select(
#    explode(
#        split(df.value, " ")
#    ).alias("word")
# )

# Generate running word count
# wordCounts = words.groupBy("word").count()

 # Start running the query that prints the running counts to the console
query = df \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()