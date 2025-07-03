from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField # FloatField retiré car numeric_price est commenté
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from models import User # Product n'est pas directement utilisé ici, mais c'est bien de l'importer si besoin futur
from config import Config

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])

    # AJOUT DU CHAMP PAYS
    # Liste de pays simplifiée. En production, utilisez une liste plus complète et standardisée.
    # Vous pourriez stocker cette liste dans config.py ou un fichier séparé.
    COUNTRY_CHOICES = [
    ('', '-- Sélectionnez votre pays --'),
    ('ZA', 'Afrique du Sud'),
    ('DZ', 'Algérie'),
    ('DE', 'Allemagne'),
    ('BE', 'Belgique'),
    ('BJ', 'Bénin'),
    ('BF', 'Burkina Faso'),
    ('CM', 'Cameroun'),
    ('CG', 'Congo-Brazzaville'),
    ('CD', 'Congo-Kinshasa (RDC)'),
    ('CI', 'Côte d\'Ivoire'),
    ('ES', 'Espagne'),
    ('FR', 'France'),
    ('GA', 'Gabon'),
    ('GH', 'Ghana'),
    ('GN', 'Guinée'),
    ('IT', 'Italie'),
    ('KE', 'Kenya'),
    ('LU', 'Luxembourg'),
    ('ML', 'Mali'),
    ('MA', 'Maroc'),
    ('NG', 'Nigéria'),
    ('NL', 'Pays-Bas'),
    ('PT', 'Portugal'),
    ('GB', 'Royaume-Uni'),
    ('SN', 'Sénégal'),
    ('SE', 'Suède'),
    ('CH', 'Suisse'),
    ('TG', 'Togo'),
    ('TN', 'Tunisie'),
    ('OTHER', 'Autre'),
]
    country = SelectField('Pays', choices=COUNTRY_CHOICES, validators=[DataRequired(message="Veuillez sélectionner votre pays.")])

    submit = SubmitField('Créer un compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

    # Optionnel: valider que le pays sélectionné n'est pas l'option vide
    def validate_country(self, country):
        if not country.data: # Si l'option vide ('') est sélectionnée
            raise ValidationError('Veuillez sélectionner un pays dans la liste.')
        
        
class ProductForm(FlaskForm):
    name = StringField('Nom du produit', validators=[DataRequired(), Length(max=100)])
    brand = StringField('Marque', validators=[Optional(), Length(max=50)])
    description = TextAreaField('Description', validators=[Optional()])
    # Assurez-vous que le label est ce que vous voulez, par ex. "Prix" au lieu de "Information sur le prix"
    price_info = StringField('Prix', default="Contacter pour prix", validators=[DataRequired(message="Le prix ou une mention est requis."), Length(max=100)]) # Changement de label et DataRequired
    image_file = FileField('Image du produit', validators=[Optional(), FileAllowed(Config.ALLOWED_EXTENSIONS, 'Images seulement!')])
    tags = StringField('Tags (séparés par des virgules)', validators=[Optional(), Length(max=200)])
    category_choices = [
        ('Non défini', 'Non défini'),
        ('Chaussures', 'Chaussures'),
        ('Sacs', 'Sacs'),
        ('Vêtements', 'Vêtements'),
        ('Montres', 'Montres'),
    ]
    category = SelectField('Catégorie Principale', choices=category_choices, default='Non défini', validators=[DataRequired(message="Veuillez sélectionner une catégorie.")])
    gender_choices = [
        ('mixte', 'mixte'),
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]
    gender = SelectField('Genre Cible', choices=gender_choices, default='Unisexe', validators=[DataRequired(message="Veuillez sélectionner un genre.")])
    submit = SubmitField('Mettre à jour Produit') 


class OrderForm(FlaskForm):
    product_name = StringField('Produit', render_kw={'readonly': True}) # Sera pré-rempli
    
    # CHAMP MODIFIÉ: S'appelle price_info maintenant
    price_info = StringField('Prix convenu (info)', validators=[DataRequired(message="Le prix est requis."), Length(max=100)])

    customer_name = StringField('Votre Nom Complet', validators=[DataRequired(), Length(max=100)])
    customer_email = StringField('Votre Email', validators=[DataRequired(), Email(), Length(max=120)])
    customer_phone = StringField('Votre Numéro de Téléphone (WhatsApp si possible)', validators=[Optional(), Length(max=30)]) # Rendu optionnel
    customer_address = TextAreaField('Votre Adresse de Livraison Complète', validators=[Optional()]) # Rendu optionnel
    quantity = IntegerField('Quantité', default=1, validators=[DataRequired(), NumberRange(min=1, message="La quantité doit être d'au moins 1.")])
    notes = TextAreaField('Notes additionnelles pour la commande', validators=[Optional()])
    submit = SubmitField('Passer la Commande')