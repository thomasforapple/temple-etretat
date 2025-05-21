import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Définir la configuration à utiliser (production, development, testing)
os.environ.setdefault('FLASK_CONFIG', 'production')

from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
