import os
from flask import Flask
from flask_login import LoginManager
from flask_caching import Cache
from pymongo import MongoClient
from app.config import config

mongo = None
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
cache = Cache()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialiser MongoDB
    global mongo
    mongo = MongoClient(app.config['MONGODB_URI'])
    app.mongo_db = mongo.get_database()
    
    # Initialiser les extensions
    login_manager.init_app(app)
    cache.init_app(app)
    
    # Créer le dossier d'uploads s'il n'existe pas
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Enregistrer les blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Vérifier si la base de données est vide et initialiser si nécessaire
    with app.app_context():
        init_db_if_empty(app)
    
    return app

def init_db_if_empty(app):
    settings_collection = app.mongo_db.settings
    sections_collection = app.mongo_db.sections
    
    # Si aucun réglage n'existe, initialiser avec les valeurs par défaut
    if settings_collection.count_documents({}) == 0:
        default_settings = {
            'site_title': 'Temple d\'Etretat',
            'colors': {
                'primary': '#3B5F7B',  # bleu gris mer
                'secondary': '#2F3A45',  # gris ardoise
                'background': '#EFE6DD',  # beige
                'accent': '#A3BFA8',  # vert nature
                'highlight': '#b04101'  # orange brique
            },
            'fonts': {
                'title': 'Rubik',
                'body': 'Nunito'
            },
            'border_radius': '12px',
            'logo': '',
            'footer_text': 'Association du Temple d\'Etretat'
        }
        settings_collection.insert_one(default_settings)
    
    # Si aucune section n'existe, initialiser avec les sections par défaut
    if sections_collection.count_documents({}) == 0:
        default_sections = [
            {
                'name': 'actuellement',
                'title': 'Actuellement',
                'content': 'Venez découvrir l\'eau et la bible et écoutez la visite commentée ici. (lien QR code pour l\'audio)',
                'order': 0,
                'visible': True,
                'images': []
            },
            {
                'name': 'nouvelles',
                'title': 'Nouvelles',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 1,
                'visible': True,
                'images': []
            },
            {
                'name': 'association',
                'title': 'Association',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 2,
                'visible': True,
                'images': []
            },
            {
                'name': 'histoire',
                'title': 'Histoire',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 3,
                'visible': True,
                'images': []
            },
            {
                'name': 'venir',
                'title': 'Venir',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 4,
                'visible': True,
                'images': []
            },
            {
                'name': 'partenaires',
                'title': 'Partenaires',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 5,
                'visible': True,
                'images': []
            },
            {
                'name': 'soutenir',
                'title': 'Nous soutenir',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'order': 6,
                'visible': True,
                'images': []
            }
        ]
        sections_collection.insert_many(default_sections)
