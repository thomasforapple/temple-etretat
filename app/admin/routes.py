from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from flask_login import login_required, current_user
from app.admin import admin
from app.admin.forms import LoginForm, SectionForm, get_image_upload_form, SettingsForm
from app.models import Section, Settings, User
from app.auth import admin_login, admin_logout, admin_required
from app import cache
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image
import datetime

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if admin_login(form.username.data, form.password.data, remember=form.remember_me.data):
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        flash('Nom d\'utilisateur ou mot de passe invalide', 'danger')
    
    # Récupérer les paramètres du site pour les styles
    settings = Settings.get()
    
    return render_template('admin/login.html', form=form, settings=settings)

@admin.route('/logout')
@login_required
def logout():
    admin_logout()
    flash('Vous avez été déconnecté', 'success')
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin_required
def dashboard():
    sections = Section.get_all()
    settings = Settings.get()
    return render_template('admin/dashboard.html', sections=sections, settings=settings)

@admin.route('/sections/reorder', methods=['POST'])
@admin_required
def reorder_sections():
    """Handle AJAX reordering of sections using drag-and-drop"""
    try:
        section_ids = request.json.get('sectionIds', [])
        if not section_ids:
            return jsonify({'success': False, 'message': 'Aucun ID de section fourni'}), 400
            
        success = Section.reorder(section_ids)
        if success:
            cache.clear()  # Vider le cache après modification
            return jsonify({'success': True, 'message': 'Ordre mis à jour avec succès'})
        return jsonify({'success': False, 'message': 'Erreur lors de la mise à jour de l\'ordre'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erreur: {str(e)}'}), 500

@admin.route('/sections/<section_id>', methods=['GET', 'POST'])
@admin_required
def edit_section(section_id):
    section = Section.get_by_id(section_id)
    if not section:
        flash('Section non trouvée', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    form = SectionForm()
    
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'content': form.content.data,
            'visible': form.visible.data
            # Removed 'order' field since we now use drag-and-drop
        }
        
        if Section.update(section_id, data):
            cache.clear()  # Vider le cache après modification
            flash('Section mise à jour avec succès', 'success')
            return redirect(url_for('admin.dashboard'))
        
        flash('Erreur lors de la mise à jour de la section', 'danger')
    
    form.title.data = section.get('title', '')
    form.content.data = section.get('content', '')
    form.visible.data = section.get('visible', True)
    
    # Créer le formulaire d'upload avec le contexte d'application actuel
    ImageUploadForm = get_image_upload_form()
    
    return render_template(
        'admin/edit_section.html', 
        form=form, 
        section=section,
        upload_form=ImageUploadForm()
    )

@admin.route('/sections/<section_id>/images', methods=['POST'])
@admin_required
def upload_image(section_id):
    section = Section.get_by_id(section_id)
    if not section:
        flash('Section non trouvée', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Créer le formulaire d'upload avec le contexte d'application actuel
    ImageUploadForm = get_image_upload_form()
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        # Ajout d'un identifiant unique pour éviter les collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Chemin complet du fichier
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Optimiser et sauvegarder l'image
        try:
            img = Image.open(file)
            # Conserver le format original ou convertir en JPEG si format non supporté
            if img.format in ['JPEG', 'PNG', 'GIF', 'WEBP']:
                format_to_save = img.format
            else:
                format_to_save = 'JPEG'
                
            # Redimensionner si trop grande
            max_size = (1200, 1200)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.LANCZOS)
            
            # Sauvegarder avec optimisation
            img.save(file_path, format=format_to_save, quality=85, optimize=True)
            
            # Créer le dictionnaire d'image
            image_data = {
                'id': uuid.uuid4().hex,
                'filename': unique_filename,
                'path': f'/uploads/{unique_filename}',
                'alt_text': form.alt_text.data,
                'caption': form.caption.data,
                'uploaded_at': datetime.datetime.now()
            }
            
            # Ajouter l'image à la section
            if Section.add_image(section_id, image_data):
                cache.clear()  # Vider le cache après modification
                flash('Image téléchargée avec succès', 'success')
            else:
                flash('Erreur lors de l\'ajout de l\'image à la section', 'danger')
                
        except Exception as e:
            flash(f'Erreur lors du traitement de l\'image: {str(e)}', 'danger')
        
        return redirect(url_for('admin.edit_section', section_id=section_id))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('admin.edit_section', section_id=section_id))

@admin.route('/sections/<section_id>/images/<image_id>/remove', methods=['POST'])
@admin_required
def remove_image(section_id, image_id):
    section = Section.get_by_id(section_id)
    if not section:
        flash('Section non trouvée', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Chercher l'image à supprimer
    image_to_remove = None
    for img in section.get('images', []):
        if img.get('id') == image_id:
            image_to_remove = img
            break
    
    if not image_to_remove:
        flash('Image non trouvée', 'danger')
        return redirect(url_for('admin.edit_section', section_id=section_id))
    
    # Supprimer le fichier physique
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_to_remove['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        flash(f'Erreur lors de la suppression du fichier: {str(e)}', 'warning')
    
    # Supprimer l'image de la section
    if Section.remove_image(section_id, image_id):
        cache.clear()  # Vider le cache après modification
        flash('Image supprimée avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de l\'image', 'danger')
    
    return redirect(url_for('admin.edit_section', section_id=section_id))

@admin.route('/settings', methods=['GET', 'POST'])
@admin_required
def edit_settings():
    form = SettingsForm()
    settings = Settings.get()
    
    if form.validate_on_submit():
        data = {
            'site_title': form.site_title.data,
            'colors': {
                'primary': form.colors.primary.data,
                'secondary': form.colors.secondary.data,
                'background': form.colors.background.data,
                'accent': form.colors.accent.data,
                'highlight': form.colors.highlight.data
            },
            'fonts': {
                'title': form.fonts.title.data,
                'body': form.fonts.body.data
            },
            'border_radius': form.border_radius.data,
            'footer_text': form.footer_text.data
        }
        
        if Settings.update(data):
            cache.clear()  # Vider le cache après modification
            flash('Paramètres mis à jour avec succès', 'success')
            return redirect(url_for('admin.edit_settings'))
        
        flash('Erreur lors de la mise à jour des paramètres', 'danger')
    
    # Pré-remplir le formulaire avec les valeurs actuelles
    if not form.is_submitted():
        form.site_title.data = settings.get('site_title', '')
        form.colors.primary.data = settings.get('colors', {}).get('primary', '#3B5F7B')
        form.colors.secondary.data = settings.get('colors', {}).get('secondary', '#2F3A45')
        form.colors.background.data = settings.get('colors', {}).get('background', '#EFE6DD')
        form.colors.accent.data = settings.get('colors', {}).get('accent', '#A3BFA8')
        form.colors.highlight.data = settings.get('colors', {}).get('highlight', '#b04101')
        form.fonts.title.data = settings.get('fonts', {}).get('title', 'Rubik')
        form.fonts.body.data = settings.get('fonts', {}).get('body', 'Nunito')
        form.border_radius.data = settings.get('border_radius', '12px')
        form.footer_text.data = settings.get('footer_text', 'Association du Temple d\'Etretat')
    
    return render_template('admin/settings.html', form=form, settings=settings)

@admin.route('/preview')
@admin_required
def preview():
    sections = Section.get_all(visible_only=True)
    settings = Settings.get()
    return render_template('main/index.html', sections=sections, settings=settings, preview=True)

@admin.route('/clear-cache')
@admin_required
def clear_cache():
    cache.clear()
    flash('Cache vidé avec succès', 'success')
    return redirect(url_for('admin.dashboard'))
