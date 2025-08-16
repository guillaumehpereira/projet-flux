from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, lit
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# 1. Créer la session Spark
spark = SparkSession.builder \
    .appName("FraudDetection") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Définir le schéma JSON des messages Kafka
schema = StructType() \
    .add("user_id", StringType()) \
    .add("transaction_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("currency", StringType()) \
    .add("timestamp", TimestampType()) \
    .add("location", StringType()) \
    .add("method", StringType())

# 3. Lire depuis Kafka (topic "transactions")
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

# 4. Parser les valeurs (en JSON)
df = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 5. Appliquer règles de détection

# Règle 1: Transactions à haute valeur (> 1000)
high_value = df.filter(col("amount") > 1000) \
    .withColumn("alert_type", lit("high_value"))

# Règle 2: Plus de 3 transactions dans une fenêtre glissante d’1 minute par utilisateur
freq_txn = df \
    .withWatermark("timestamp", "5 minutes") \
    .groupBy(window(col("timestamp"), "1 minute"), col("user_id")) \
    .count() \
    .filter(col("count") > 3) \
    .select(col("user_id"), col("window.start").alias("timestamp")) \
    .withColumn("alert_type", lit("frequent_txn"))

# Règle 3: Transactions dans plusieurs localisations (villes) différentes dans une fenêtre de 5 minutes
loc_count = df \
    .withWatermark("timestamp", "5 minutes") \
    .dropDuplicates(["user_id", "location", "timestamp"]) \
    .groupBy(window(col("timestamp"), "5 minutes"), col("user_id")) \
    .count() \
    .filter(col("count") > 1) \
    .select(col("user_id"), col("window.start").alias("timestamp")) \
    .withColumn("alert_type", lit("multi_location"))

# 6. Fusionner toutes les alertes
alerts = high_value.select("user_id", "transaction_id", "amount", "timestamp", "alert_type") \
    .unionByName(freq_txn.select("user_id", lit(None).alias("transaction_id"), lit(None).alias("amount"), "timestamp", "alert_type")) \
    .unionByName(loc_count.select("user_id", lit(None).alias("transaction_id"), lit(None).alias("amount"), "timestamp", "alert_type"))

# 7. Écriture vers la console (debug)
query_console = alerts.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# 8. Écriture vers Kafka (topic fraud-alerts)
query_kafka = alerts \
    .selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "fraud-alerts") \
    .option("checkpointLocation", "/tmp/checkpoint-kafka") \
    .outputMode("append") \
    .start()

# 9. Écriture vers fichier Parquet
query_parquet = alerts.writeStream \
    .format("parquet") \
    .option("path", "/tmp/fraud_alerts_parquet") \
    .option("checkpointLocation", "/tmp/checkpoint-parquet") \
    .outputMode("append") \
    .start()

# Attendre la fin des requêtes
query_console.awaitTermination()
query_kafka.awaitTermination()
query_parquet.awaitTermination()
