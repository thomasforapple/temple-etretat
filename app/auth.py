from flask import current_app, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from functools import wraps
from app.models import User
import datetime

def admin_login(username, password, remember=False):
    user = User.get_by_username(username)
    
    if not user or not user.verify_password(password):
        return False
    
    login_user(user, remember=remember)
    user.update_last_login()
    return True

def admin_logout():
    logout_user()
    
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
