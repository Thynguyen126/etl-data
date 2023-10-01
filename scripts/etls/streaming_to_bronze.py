from pyspark.sql import SparkSession
import pyspark.sql.functions as sf
from pyspark.sql.types import * 


spark = SparkSession.builder \
   .appName("streaming_to_bronze") \
   .config("spark.driver.host", "localhost") \
   .getOrCreate()

spark.sparkContext.setLogLevel("WARN")



# Create DataFrame representing the stream of input lines from kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "orders") \
  .load()

order_schema = StructType([
  StructField("order_code", IntegerType(), False),
  StructField("distance", FloatType(), True),
  StructField("final_deli_supplier", StringType(), True),
  StructField("destination_region", StringType(), True),
  StructField("destination_district", StringType(), True),
  StructField("departure_region", StringType(), True),
  StructField("seller_id", IntegerType(), False),
  StructField("route", StringType(), True),
  StructField("product_id", IntegerType(), False),
  StructField("created_at", TimestampType(), True)
])

df2 = df.selectExpr("CAST(value AS STRING)") \
  .withColumn("value_json", sf.from_json(sf.col("value").cast("string"), order_schema)) \
  .select("value_json.*")


# Split the lines into words
# words = df.select(
#    explode(
#        split(df.value, " ")
#    ).alias("word")
# )

# Generate running word count
# wordCounts = words.groupBy("word").count()


def _write_streaming(df, epoch_id) -> None:         

    df.write \
        .mode('append') \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://postgres:5432/db_bronze_zone") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", 'orders') \
        .option("user", 'postgres') \
        .option("password", 'admin@123') \
        .save()

 # Start running the query that prints the running counts to the console
query = df2 \
    .writeStream \
    .foreachBatch(_write_streaming) \
    .start()

query.awaitTermination()