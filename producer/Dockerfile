# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copie les fichiers nécessaires
COPY kafka_producer.py requirements.txt ./

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["python", "kafka_producer.py"]

