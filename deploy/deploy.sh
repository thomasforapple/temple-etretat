#!/bin/bash

# Script de déploiement pour l'application Temple d'Etretat
# Usage: ./deploy.sh [--initial]

# Vérifier si c'est un déploiement initial
INITIAL=false
if [ "$1" == "--initial" ]; then
    INITIAL=true
fi

# Configuration des chemins
APP_NAME="temple-etretat"
APP_PATH="/home/ubuntu/apps/$APP_NAME"
LOG_PATH="$APP_PATH/logs"
REPO_URL="<votre-repo-git>"  # Remplacer par votre URL de dépôt
BRANCH="main"

# Créer les dossiers nécessaires lors du déploiement initial
if [ "$INITIAL" = true ]; then
    echo "Configuration initiale..."
    mkdir -p $APP_PATH
    mkdir -p $LOG_PATH
    
    # Cloner le dépôt
    echo "Clonage du dépôt..."
    git clone -b $BRANCH $REPO_URL $APP_PATH
    
    # Créer l'environnement virtuel
    echo "Création de l'environnement virtuel..."
    python3 -m venv $APP_PATH/venv
    
    # Installer les dépendances
    echo "Installation des dépendances..."
    $APP_PATH/venv/bin/pip install -r $APP_PATH/requirements.txt
    $APP_PATH/venv/bin/pip install gunicorn
    
    # Copier le fichier .env d'exemple
    cp $APP_PATH/.env.example $APP_PATH/.env
    echo "Veuillez modifier le fichier .env avec vos paramètres"
    
    # Configurer Supervisor
    echo "Configuration de Supervisor..."
    sudo cp $APP_PATH/deploy/supervisor.conf /etc/supervisor/conf.d/$APP_NAME.conf
    sudo supervisorctl reread
    sudo supervisorctl update
    
    # Configurer Nginx
    echo "Configuration de Nginx..."
    sudo cp $APP_PATH/deploy/nginx.conf /etc/nginx/sites-available/$APP_NAME
    sudo ln -s /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    
    echo "Configuration initiale terminée."
    echo "N'oubliez pas de modifier le fichier .env avec vos paramètres."
    echo "Pour obtenir un certificat SSL, exécutez :"
    echo "sudo certbot --nginx -d temple-etretat.fr -d www.temple-etretat.fr"
else
    # Mise à jour du code depuis le dépôt
    echo "Mise à jour du code..."
    cd $APP_PATH
    git pull origin $BRANCH
    
    # Mise à jour des dépendances
    echo "Mise à jour des dépendances..."
    $APP_PATH/venv/bin/pip install -r $APP_PATH/requirements.txt
    
    # Redémarrer le service
    echo "Redémarrage du service..."
    sudo supervisorctl restart $APP_NAME
    
    echo "Déploiement terminé."
fi