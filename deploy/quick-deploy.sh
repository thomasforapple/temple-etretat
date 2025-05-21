#!/bin/bash

# Script de déploiement rapide pour l'application Temple d'Etretat
# Ce script est conçu pour être exécuté depuis votre machine locale pour
# pousser rapidement les modifications vers le serveur.

# Configuration
SERVER="ubuntu@votre-serveur.com"  
APP_PATH="/home/ubuntu/apps/temple-etretat"
BRANCH="main"

echo "Déploiement rapide vers $SERVER..."

# Pousser les modifications vers le dépôt Git
echo "Commit et push des modifications..."
git add .
git commit -m "Quick update: $(date +"%Y-%m-%d %H:%M")"
git push origin $BRANCH

# Exécuter le script de déploiement sur le serveur
echo "Déploiement sur le serveur..."
ssh $SERVER "cd $APP_PATH && ./deploy/deploy.sh"

echo "Déploiement rapide terminé."