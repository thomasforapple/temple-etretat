from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, HiddenField, SubmitField, FormField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from flask import current_app

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class SectionForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    visible = BooleanField('Visible', default=True)
    # Removed order field
    submit = SubmitField('Enregistrer')

# Définir une fonction qui crée le formulaire avec le contexte d'application
def get_image_upload_form():
    # Cette fonction sera appelée dans les routes, avec le contexte d'application
    class ImageUploadForm(FlaskForm):
        image = FileField('Image', validators=[
            FileRequired(),
            FileAllowed(current_app.config['ALLOWED_EXTENSIONS'], 'Images uniquement !')
        ])
        alt_text = StringField('Texte alternatif', validators=[DataRequired()])
        caption = StringField('Légende', validators=[Optional()])
        submit = SubmitField('Télécharger')
    
    return ImageUploadForm

class ColorForm(FlaskForm):
    primary = StringField('Couleur principale', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ])
    secondary = StringField('Couleur secondaire', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ])
    background = StringField('Couleur de fond', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ])
    accent = StringField('Couleur d\'accent', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ])
    highlight = StringField('Couleur de surbrillance', validators=[
        DataRequired(), 
        Regexp(r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Format hexadécimal invalide')
    ])

class FontsForm(FlaskForm):
    title = SelectField('Police des titres', choices=[
        ('Rubik', 'Rubik'),
        ('Montserrat', 'Montserrat'),
        ('Playfair Display', 'Playfair Display'),
        ('Raleway', 'Raleway'),
        ('Lora', 'Lora')
    ])
    body = SelectField('Police du corps de texte', choices=[
        ('Nunito', 'Nunito'),
        ('Open Sans', 'Open Sans'),
        ('Roboto', 'Roboto'),
        ('Source Sans Pro', 'Source Sans Pro'),
        ('Lato', 'Lato')
    ])

class SettingsForm(FlaskForm):
    site_title = StringField('Titre du site', validators=[DataRequired()])
    colors = FormField(ColorForm)
    fonts = FormField(FontsForm)
    border_radius = StringField('Arrondi des bordures', validators=[DataRequired()])
    footer_text = StringField('Texte de pied de page', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')