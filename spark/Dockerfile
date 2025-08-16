# Dockerfile pour Spark + connecteur Kafka avec commons-pool2

FROM bitnami/spark:3.5

# Crée le dossier de travail
WORKDIR /app

# Copie le script Spark
COPY spark_job.py .

# Télécharge les JARs nécessaires pour Kafka + dépendance commons-pool2
RUN mkdir -p /opt/bitnami/spark/jars && \
    curl -L -o /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/kafka-clients-3.5.0.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/bitnami/spark/jars/commons-pool2-2.11.1.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# Lancement du job Spark avec tous les JARs nécessaires
CMD ["spark-submit", "--jars", "/opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar,/opt/bitnami/spark/jars/kafka-clients-3.5.0.jar,/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar,/opt/bitnami/spark/jars/commons-pool2-2.11.1.jar", "/app/spark_job.py"]
