#!/bin/bash

echo "Réinitialisation complète du projet..."

# 1. Arrêter les services
docker-compose down

# 2. Supprimer les volumes Docker
docker volume rm $(docker volume ls -qf dangling=false)

# 3. Supprimer les fichiers Parquet locaux
rm -rf parquet_data/*

echo "Réinitialisation terminée."