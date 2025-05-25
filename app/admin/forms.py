from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, HiddenField, SubmitField, FormField, Form, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, NumberRange, URL
from flask import current_app

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class SectionForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Contenu', validators=[DataRequired()], 
                          render_kw={"placeholder": "Utilisez l'éditeur avancé pour créer du contenu riche avec mise en forme, images et styles personnalisés..."})
    visible = BooleanField('Visible', default=True)
    submit = SubmitField('Enregistrer')

# Enhanced image upload form with advanced options
def get_image_upload_form():
    class ImageUploadForm(FlaskForm):
        image = FileField('Image(s)', validators=[
            FileRequired(message="Veuillez sélectionner au moins une image"),
            FileAllowed(current_app.config['ALLOWED_EXTENSIONS'], 
                       'Formats supportés: JPG, PNG, GIF, SVG, WebP uniquement!')
        ], render_kw={
            "multiple": True,
            "accept": "image/*",
            "class": "form-control"
        })
        
        alt_text = StringField('Texte alternatif', validators=[
            DataRequired(message="Le texte alternatif est obligatoire pour l'accessibilité")
        ], render_kw={
            "placeholder": "Description de l'image pour les lecteurs d'écran"
        })
        
        caption = StringField('Légende', validators=[Optional(), Length(max=500)], 
                            render_kw={
                                "placeholder": "Légende visible sous l'image (optionnel)"
                            })
        
        # Enhanced size options
        size = SelectField('Taille d\'affichage', choices=[
            ('thumbnail', '🔍 Miniature (150px)'),
            ('small', '📱 Petite (25%)'),
            ('medium', '💻 Moyenne (50%)'),
            ('large', '🖥️ Grande (75%)'),
            ('full', '📺 Pleine largeur (100%)'),
            ('custom', '⚙️ Personnalisée')
        ], default='medium')
        
        custom_width = IntegerField('Largeur personnalisée (px)', validators=[
            Optional(), NumberRange(min=50, max=2000)
        ], render_kw={"placeholder": "ex: 400"})
        
        custom_height = IntegerField('Hauteur personnalisée (px)', validators=[
            Optional(), NumberRange(min=50, max=2000)
        ], render_kw={"placeholder": "ex: 300 (optionnel)"})
        
        # Enhanced alignment options
        alignment = SelectField('Alignement', choices=[
            ('left', '⬅️ Gauche'),
            ('center', '⬆️ Centre'),
            ('right', '➡️ Droite'),
            ('float-left', '🔄 Flottant gauche'),
            ('float-right', '🔃 Flottant droite')
        ], default='center')
        
        # Enhanced shape options
        shape = SelectField('Style visuel', choices=[
            ('default', '📷 Rectangulaire'),
            ('rounded', '📐 Coins arrondis'),
            ('circle', '⭕ Cercle'),
            ('shadow', '🎭 Avec ombre'),
            ('border', '🖼️ Avec bordure'),
            ('polaroid', '📸 Style Polaroid'),
            ('vintage', '🎞️ Style vintage')
        ], default='default')
        
        # Link options
        link_url = StringField('URL de destination', validators=[
            Optional(), URL(message="Veuillez entrer une URL valide")
        ], render_kw={
            "placeholder": "https://exemple.com (rend l'image cliquable)"
        })
        
        link_target = SelectField('Ouverture du lien', choices=[
            ('_self', 'Même fenêtre'),
            ('_blank', 'Nouvelle fenêtre/onglet')
        ], default='_blank')
        
        # Gallery options
        gallery_group = StringField('Groupe de galerie', validators=[
            Optional(), Length(max=100)
        ], render_kw={
            "placeholder": "ex: expo2024, portraits, paysages"
        })
        
        gallery_order = IntegerField('Ordre dans la galerie', validators=[
            Optional(), NumberRange(min=0, max=999)
        ], default=0)
        
        # SEO and accessibility
        seo_title = StringField('Titre SEO', validators=[
            Optional(), Length(max=100)
        ], render_kw={
            "placeholder": "Titre pour les moteurs de recherche"
        })
        
        # Advanced display options
        lazy_loading = BooleanField('Chargement différé', default=True,
                                  description="Améliore les performances en chargeant l'image seulement quand nécessaire")
        
        responsive = BooleanField('Responsive', default=True,
                                description="Adapte automatiquement la taille sur mobile")
        
        # Image quality and optimization
        quality = SelectField('Qualité de compression', choices=[
            ('high', '🔥 Haute qualité (moins compressée)'),
            ('medium', '⚖️ Qualité moyenne (équilibrée)'),
            ('low', '💨 Qualité réduite (très compressée)')
        ], default='medium')
        
        # Watermark option
        add_watermark = BooleanField('Ajouter un filigrane',
                                   description="Ajoute le logo du site en filigrane")
        
        submit = SubmitField('📤 Télécharger l\'image')
    
    return ImageUploadForm

# Enhanced image editing form
def get_image_edit_form():
    class ImageEditForm(FlaskForm):
        alt_text = StringField('Texte alternatif', validators=[
            DataRequired(message="Le texte alternatif est obligatoire")
        ])
        
        caption = StringField('Légende', validators=[Optional(), Length(max=500)])
        
        # Same enhanced options as upload form
        size = SelectField('Taille d\'affichage', choices=[
            ('thumbnail', '🔍 Miniature (150px)'),
            ('small', '📱 Petite (25%)'),
            ('medium', '💻 Moyenne (50%)'),
            ('large', '🖥️ Grande (75%)'),
            ('full', '📺 Pleine largeur (100%)'),
            ('custom', '⚙️ Personnalisée')
        ])
        
        custom_width = IntegerField('Largeur personnalisée (px)', validators=[
            Optional(), NumberRange(min=50, max=2000)
        ])
        
        custom_height = IntegerField('Hauteur personnalisée (px)', validators=[
            Optional(), NumberRange(min=50, max=2000)
        ])
        
        alignment = SelectField('Alignement', choices=[
            ('left', '⬅️ Gauche'),
            ('center', '⬆️ Centre'),
            ('right', '➡️ Droite'),
            ('float-left', '🔄 Flottant gauche'),
            ('float-right', '🔃 Flottant droite')
        ])
        
        shape = SelectField('Style visuel', choices=[
            ('default', '📷 Rectangulaire'),
            ('rounded', '📐 Coins arrondis'),
            ('circle', '⭕ Cercle'),
            ('shadow', '🎭 Avec ombre'),
            ('border', '🖼️ Avec bordure'),
            ('polaroid', '📸 Style Polaroid'),
            ('vintage', '🎞️ Style vintage')
        ])
        
        link_url = StringField('URL de destination', validators=[
            Optional(), URL(message="Veuillez entrer une URL valide")
        ])
        
        link_target = SelectField('Ouverture du lien', choices=[
            ('_self', 'Même fenêtre'),
            ('_blank', 'Nouvelle fenêtre/onglet')
        ])
        
        gallery_group = StringField('Groupe de galerie', validators=[
            Optional(), Length(max=100)
        ])
        
        gallery_order = IntegerField('Ordre dans la galerie', validators=[
            Optional(), NumberRange(min=0, max=999)
        ])
        
        seo_title = StringField('Titre SEO', validators=[
            Optional(), Length(max=100)
        ])
        
        lazy_loading = BooleanField('Chargement différé', default=True)
        responsive = BooleanField('Responsive', default=True)
        
        # Image transformation options
        rotate = SelectField('Rotation', choices=[
            ('0', 'Aucune rotation'),
            ('90', '90° droite'),
            ('180', '180°'),
            ('270', '90° gauche')
        ], default='0')
        
        flip = SelectField('Retournement', choices=[
            ('none', 'Aucun'),
            ('horizontal', 'Horizontal'),
            ('vertical', 'Vertical'),
            ('both', 'Horizontal et vertical')
        ], default='none')
        
        # Filter effects
        filter_effect = SelectField('Effet de filtre', choices=[
            ('none', 'Aucun effet'),
            ('grayscale', '⚫ Noir et blanc'),
            ('sepia', '🟤 Sépia'),
            ('blur', '😵 Flou'),
            ('brightness', '☀️ Plus lumineux'),
            ('contrast', '🎭 Contraste élevé'),
            ('vintage', '📷 Vintage'),
            ('warm', '🔥 Tons chauds'),
            ('cool', '❄️ Tons froids')
        ], default='none')
        
        submit = SubmitField('💾 Mettre à jour l\'image')
    
    return ImageEditForm

# Enhanced color form for settings
class ColorForm(Form):
    primary = StringField('Couleur principale', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide (ex: #FF0000)')
    ], render_kw={"type": "color"})
    
    secondary = StringField('Couleur secondaire', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ], render_kw={"type": "color"})
    
    background = StringField('Couleur de fond', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ], render_kw={"type": "color"})
    
    accent = StringField('Couleur d\'accent', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ], render_kw={"type": "color"})
    
    highlight = StringField('Couleur de surbrillance', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ], render_kw={"type": "color"})

# Enhanced fonts form
class FontsForm(Form):
    title = SelectField('Police des titres', choices=[
        ('Rubik', 'Rubik (moderne et claire)'),
        ('Montserrat', 'Montserrat (élégante)'),
        ('Playfair Display', 'Playfair Display (classique)'),
        ('Raleway', 'Raleway (minimaliste)'),
        ('Lora', 'Lora (lecture agréable)'),
        ('Inter', 'Inter (très lisible)'),
        ('Poppins', 'Poppins (géométrique)'),
        ('Source Sans Pro', 'Source Sans Pro (professionnelle)')
    ])
    
    body = SelectField('Police du corps de texte', choices=[
        ('Nunito', 'Nunito (arrondie et douce)'),
        ('Open Sans', 'Open Sans (universelle)'),
        ('Roboto', 'Roboto (moderne)'),
        ('Source Sans Pro', 'Source Sans Pro (claire)'),
        ('Lato', 'Lato (harmonieuse)'),
        ('IBM Plex Sans', 'IBM Plex Sans (technique)'),
        ('Inter', 'Inter (optimisée écrans)'),
        ('Noto Sans', 'Noto Sans (multilingue)')
    ])

# Enhanced settings form
class SettingsForm(FlaskForm):
    site_title = StringField('Titre du site', validators=[
        DataRequired(), Length(min=1, max=100)
    ], render_kw={"placeholder": "Temple d'Etretat"})
    
    site_description = TextAreaField('Description du site', validators=[
        Optional(), Length(max=500)
    ], render_kw={
        "placeholder": "Description pour les moteurs de recherche et réseaux sociaux",
        "rows": 3
    })
    
    colors = FormField(ColorForm)
    fonts = FormField(FontsForm)
    
    # Enhanced typography options
    base_font_size = SelectField('Taille de police de base', choices=[
        ('14px', 'Petite (14px)'),
        ('15px', 'Normale (15px)'),
        ('16px', 'Standard (16px)'),
        ('17px', 'Grande (17px)'),
        ('18px', 'Très grande (18px)')
    ], default='16px')
    
    line_height = SelectField('Hauteur de ligne', choices=[
        ('1.4', 'Compacte (1.4)'),
        ('1.5', 'Normale (1.5)'),
        ('1.6', 'Confortable (1.6)'),
        ('1.7', 'Aérée (1.7)'),
        ('1.8', 'Très aérée (1.8)')
    ], default='1.6')
    
    border_radius = StringField('Arrondi des bordures', validators=[
        DataRequired(), Regexp(r'^\d+(px|rem|em|%)$', 
                             message='Format invalide (ex: 12px, 1rem)')
    ], render_kw={"placeholder": "12px"})
    
    # Enhanced layout options
    max_width = SelectField('Largeur maximale du contenu', choices=[
        ('1000px', 'Étroite (1000px)'),
        ('1200px', 'Standard (1200px)'),
        ('1400px', 'Large (1400px)'),
        ('1600px', 'Très large (1600px)'),
        ('100%', 'Pleine largeur')
    ], default='1200px')
    
    # Social media and SEO
    logo_url = StringField('URL du logo', validators=[
        Optional(), URL(message="URL invalide")
    ], render_kw={"placeholder": "https://exemple.com/logo.png"})
    
    favicon_url = StringField('URL du favicon', validators=[
        Optional(), URL(message="URL invalide")
    ], render_kw={"placeholder": "https://exemple.com/favicon.ico"})
    
    # Contact information
    footer_text = StringField('Texte de pied de page', validators=[
        DataRequired(), Length(max=200)
    ], render_kw={"placeholder": "Association du Temple d'Etretat"})
    
    contact_email = StringField('Email de contact', validators=[
        Optional(), Email(message="Email invalide")
    ], render_kw={"placeholder": "contact@temple-etretat.fr"})
    
    phone_number = StringField('Numéro de téléphone', validators=[
        Optional(), Length(max=20)
    ], render_kw={"placeholder": "+33 1 23 45 67 89"})
    
    address = TextAreaField('Adresse', validators=[
        Optional(), Length(max=300)
    ], render_kw={
        "placeholder": "Adresse complète du temple",
        "rows": 3
    })
    
    # Social media links
    facebook_url = StringField('Facebook', validators=[
        Optional(), URL(message="URL Facebook invalide")
    ], render_kw={"placeholder": "https://facebook.com/temple.etretat"})
    
    instagram_url = StringField('Instagram', validators=[
        Optional(), URL(message="URL Instagram invalide")
    ], render_kw={"placeholder": "https://instagram.com/temple.etretat"})
    
    youtube_url = StringField('YouTube', validators=[
        Optional(), URL(message="URL YouTube invalide")
    ], render_kw={"placeholder": "https://youtube.com/temple.etretat"})
    
    # Advanced settings
    enable_comments = BooleanField('Activer les commentaires', default=False)
    enable_search = BooleanField('Activer la recherche', default=True)
    enable_analytics = BooleanField('Activer Google Analytics', default=False)
    
    analytics_id = StringField('ID Google Analytics', validators=[
        Optional(), Regexp(r'^G-[A-Z0-9]+$|^UA-\d+-\d+$', 
                          message='Format Google Analytics invalide')
    ], render_kw={"placeholder": "G-XXXXXXXXXX"})
    
    # Performance settings
    enable_caching = BooleanField('Activer le cache', default=True,
                                description="Améliore les performances du site")
    
    cache_duration = SelectField('Durée du cache', choices=[
        ('300', '5 minutes'),
        ('900', '15 minutes'),
        ('1800', '30 minutes'),
        ('3600', '1 heure'),
        ('7200', '2 heures')
    ], default='300')
    
    # Maintenance mode
    maintenance_mode = BooleanField('Mode maintenance', default=False,
                                  description="Affiche une page de maintenance aux visiteurs")
    
    maintenance_message = TextAreaField('Message de maintenance', validators=[
        Optional(), Length(max=1000)
    ], render_kw={
        "placeholder": "Le site est temporairement en maintenance. Nous reviendrons bientôt !",
        "rows": 3
    })
    
    submit = SubmitField('💾 Enregistrer les paramètres')

# Advanced search form for content
class SearchForm(FlaskForm):
    query = StringField('Recherche', validators=[
        DataRequired(), Length(min=2, max=100)
    ], render_kw={
        "placeholder": "Rechercher dans le contenu...",
        "autocomplete": "off"
    })
    
    section_filter = SelectField('Dans la section', choices=[
        ('all', 'Toutes les sections'),
        ('actuellement', 'Actuellement'),
        ('nouvelles', 'Nouvelles'),
        ('association', 'Association'),
        ('histoire', 'Histoire'),
        ('venir', 'Venir'),
        ('partenaires', 'Partenaires'),
        ('soutenir', 'Nous soutenir')
    ], default='all')
    
    content_type = SelectField('Type de contenu', choices=[
        ('all', 'Tout le contenu'),
        ('text', 'Texte seulement'),
        ('images', 'Images seulement')
    ], default='all')
    
    submit = SubmitField('🔍 Rechercher')

# Backup and export form
class BackupForm(FlaskForm):
    include_images = BooleanField('Inclure les images', default=True)
    include_settings = BooleanField('Inclure les paramètres', default=True)
    
    backup_format = SelectField('Format de sauvegarde', choices=[
        ('json', 'JSON (recommandé)'),
        ('csv', 'CSV (pour Excel)'),
        ('xml', 'XML')
    ], default='json')
    
    submit = SubmitField('💾 Créer une sauvegarde')

# Import form
class ImportForm(FlaskForm):
    backup_file = FileField('Fichier de sauvegarde', validators=[
        FileRequired(),
        FileAllowed(['json', 'csv', 'xml'], 'Formats supportés: JSON, CSV, XML')
    ])
    
    overwrite_existing = BooleanField('Remplacer le contenu existant', 
                                    description="⚠️ Attention: ceci supprimera tout le contenu actuel")
    
    submit = SubmitField('📤 Importer')
