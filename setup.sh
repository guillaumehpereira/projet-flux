#!/bin/bash

echo "Initialisation du projet Real-Time Fraud Detection..."

# Étape 1 : Build des images Docker
echo "🔧 Construction des images Docker..."
docker-compose build

# Étape 2 : Lancement des conteneurs
echo "Démarrage des services Docker..."
docker-compose up -d

# Étape 3 : Résumé
echo ""
echo "Projet lancé avec succès !"
echo ""
echo "Accès rapide :"
echo "   - Kafka      : bootstrap à kafka:9092"
echo "   - Kafdrop    : http://localhost:9000"
echo "   - Parquet    : ./parquet_data/"
echo "   - Dashboard  : http://localhost:8501"
echo ""
echo "Pour arrêter le projet : docker-compose down"