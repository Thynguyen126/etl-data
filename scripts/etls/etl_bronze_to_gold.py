from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .config("spark.driver.host", "localhost")\
    .getOrCreate()


# Create DataFrame representing the stream of input lines from kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "demo") \
  .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Split the lines into words
words = df.select(
   explode(
       split(df.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

 # Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()