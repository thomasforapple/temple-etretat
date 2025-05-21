from flask import render_template, current_app, send_from_directory, abort
from app.models import Section, Settings
from app.main import main
from app import cache
import os

@main.route('/')
@cache.cached(timeout=300)  # Cache la page d'accueil pendant 5 minutes
def index():
    sections = Section.get_all(visible_only=True)
    settings = Settings.get()
    return render_template('main/index.html', sections=sections, settings=settings)

@main.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except:
        abort(404)

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

@main.route('/robots.txt')
def robots():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'robots.txt', mimetype='text/plain'
    )

@main.app_errorhandler(404)
def page_not_found(e):
    settings = Settings.get()
    return render_template('main/404.html', settings=settings), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    settings = Settings.get()
    return render_template('main/500.html', settings=settings), 500
