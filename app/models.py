from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import login_manager
import datetime
import os

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.username = user_data.get('username')
        self.password_hash = user_data.get('password_hash')
        self.email = user_data.get('email')
        self.last_login = user_data.get('last_login')
    
    @staticmethod
    def create(username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password, method='pbkdf2:sha256'),
            'created_at': datetime.datetime.now(),
            'last_login': None
        }
        result = current_app.mongo_db.users.insert_one(user_data)
        return User.get_by_id(str(result.inserted_id))
    
    @staticmethod
    def get_by_id(user_id):
        try:
            user_data = current_app.mongo_db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User(user_data)
        except:
            return None
    
    @staticmethod
    def get_by_username(username):
        user_data = current_app.mongo_db.users.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None
    
    def verify_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except ValueError as e:
            if "unsupported hash type" in str(e) and "scrypt" in str(e):
                # For existing scrypt hashes, check against temporary password
                temp_password = os.environ.get('TEMP_ADMIN_PASSWORD')
                
                if temp_password and password == temp_password:
                    # Update the password hash to a supported format
                    self.update_password_hash(password)
                    return True
                return False
            raise e
    
    def update_password_hash(self, password):
        """Update user's password hash to a supported format"""
        new_hash = generate_password_hash(password, method='pbkdf2:sha256')
        current_app.mongo_db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'password_hash': new_hash}}
        )
        self.password_hash = new_hash
    
    def update_last_login(self):
        current_app.mongo_db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'last_login': datetime.datetime.now()}}
        )

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class Section:
    @staticmethod
    def get_all(visible_only=False):
        query = {}
        if visible_only:
            query['visible'] = True
        
        sections = list(current_app.mongo_db.sections.find(query).sort('order', 1))
        return sections
    
    @staticmethod
    def get_by_name(name):
        return current_app.mongo_db.sections.find_one({'name': name})
    
    @staticmethod
    def get_by_id(section_id):
        try:
            return current_app.mongo_db.sections.find_one({'_id': ObjectId(section_id)})
        except:
            return None
    
    @staticmethod
    def update(section_id, data):
        try:
            current_app.mongo_db.sections.update_one(
                {'_id': ObjectId(section_id)},
                {'$set': data}
            )
            return True
        except:
            return False
    
    @staticmethod
    def reorder(section_ids):
        """Update the order of sections based on the provided list of IDs"""
        try:
            for index, section_id in enumerate(section_ids):
                current_app.mongo_db.sections.update_one(
                    {'_id': ObjectId(section_id)},
                    {'$set': {'order': index}}
                )
            return True
        except Exception as e:
            print(f"Error reordering sections: {str(e)}")
            return False
    
    @staticmethod
    def add_image(section_id, image_data):
        try:
            current_app.mongo_db.sections.update_one(
                {'_id': ObjectId(section_id)},
                {'$push': {'images': image_data}}
            )
            return True
        except:
            return False
    
    @staticmethod
    def remove_image(section_id, image_id):
        try:
            current_app.mongo_db.sections.update_one(
                {'_id': ObjectId(section_id)},
                {'$pull': {'images': {'id': image_id}}}
            )
            return True
        except:
            return False
class Settings:
    @staticmethod
    def get():
        settings = current_app.mongo_db.settings.find_one()
        if not settings:
            # Initialiser avec des valeurs par défaut
            settings = {
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
            current_app.mongo_db.settings.insert_one(settings)
        
        return settings
    
    @staticmethod
    def update(data):
        try:
            # Add debugging info
            print(f"Updating settings with data: {data}")
            
            # Find existing settings
            settings = current_app.mongo_db.settings.find_one()
            
            if settings:
                # Perform the update
                result = current_app.mongo_db.settings.update_one(
                    {'_id': settings['_id']},
                    {'$set': data}
                )
                
                # Check if update was successful
                print(f"Update operation details: matched={result.matched_count}, modified={result.modified_count}")
                return True
            else:
                # Insert new settings if none exist
                result = current_app.mongo_db.settings.insert_one(data)
                print(f"New settings created with ID: {result.inserted_id}")
                return True
                
        except Exception as e:
            print(f"Error updating settings: {str(e)}")
            import traceback
            traceback.print_exc()
            return False