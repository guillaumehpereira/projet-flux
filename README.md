# Real-Time Fraud Detection Pipeline

Ce projet implémente un pipeline temps réel de détection de fraudes basé sur Kafka, Spark Structured Streaming et un dashboard Streamlit.

---

## Contenu du projet

- **Producteur Kafka (Python)** : simule des transactions bancaires en temps réel
- **Spark Structured Streaming** : détecte les fraudes selon 3 règles
- **Kafka (KRaft)** : utilisé comme système de transport d’événements (sans ZooKeeper)
- **Dashboard Streamlit** : visualisation des alertes de fraude détectées
- **Kafdrop** : interface web pour inspecter les topics Kafka
- **Docker** : orchestration complète via Docker Compose

---

## Lancement du pipeline
```bash
./setup.sh
```

Ce script :
- build les images Docker
- lance Kafka, le producteur, Spark et le dashboard
- crée les dossiers nécessaires

---

## Accès rapide

| Service      | URL / Info                     |
|--------------|--------------------------------|
| Kafka Broker | `kafka:9092` (interne)         |
| Kafdrop      | http://localhost:9000          |
| Dashboard    | http://localhost:8501          |
| Parquet data | `./parquet_data/`              |

---

## Détection de fraudes

Les règles appliquées dans le pipeline Spark sont :

1. **Transaction à haute valeur** > 1000€
2. **Plus de 3 transactions** par utilisateur en moins d’1 minute
3. **Transactions dans plusieurs localisations** en moins de 5 minutes

---

## Structure du projet

```
projet-flux/
├── producer/             # Producteur Kafka Python
│   ├── kafka_producer.py
│   ├── requirements.txt
│   └── Dockerfile
├── spark/                # Job Spark Streaming
│   ├── spark_job.py
│   └── Dockerfile
├── dashboard/            # Interface Streamlit
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── parquet_data/         # Fichiers Parquet générés
├── docker-compose.yml
├── setup.sh              # Script de lancement
└── README.md
```

---

## Tests et démonstration

- Les transactions sont produites à un rythme de 10 à 100 événements par seconde
- Les alertes sont affichées :
  - dans la **console Spark**
  - dans le topic Kafka `fraud-alerts`
  - dans le dossier `parquet_data/`
  - dans le **dashboard interactif Streamlit**

Des **captures d’écran** illustrant ces résultats sont disponibles dans le dossier `outputs_visuals/` incluant :
  - des extraits de logs et de messages Kafka (via Kafdrop),
  - un aperçu des fichiers Parquet générés,
  - des vues du dashboard Streamlit avec tableau et graphiques.

---

## Arrêter le projet

```bash
docker-compose down
```

## Remise à zéro du projet
```bash
./reset.sh
```
---

## Critères respectés

| Élement                           | OK?|
|-----------------------------------|----|
| Kafka producer                    | OK |
| Spark Streaming                   | OK |
| Parsing JSON + schéma             | OK |
| 3 règles de fraude                | OK |
| Sortie console, Kafka, Parquet    | OK |
| Dockerisation complète            | OK |
| Dashboard interactif (bonus)      | OK |

---