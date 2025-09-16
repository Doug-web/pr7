## --- START OF FILE config.py ---

import os

# Le BASE_DIR pointe vers le dossier racine de votre application
# C'est la base pour construire des chemins absolus et fiables
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clé secrète pour la sécurité des sessions Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete_tres_difficile_a_deviner'
    
    # --- CONFIGURATION DE LA BASE DE DONNÉES SQLITE ---
    # On supprime toute la logique complexe pour PostgreSQL/Render.
    # On définit simplement un chemin pour notre fichier de base de données local.
    # os.path.join() crée un chemin compatible avec tous les systèmes d'exploitation (Windows, Mac, Linux).
    # Le fichier 'stock.db' sera créé à la racine de votre projet, à côté de ce fichier config.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'stock.db')

    # Désactive une fonctionnalité de Flask-SQLAlchemy qui n'est plus nécessaire et consomme des ressources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- LES AUTRES CONFIGURATIONS RESTENT INCHANGÉES ---
    # Ces configurations sont toujours utiles pour votre application, même avec SQLite.

    # Chemin pour les fichiers uploadés (disque persistant sur Render ou dossier local)
    UPLOADS_BASE_PATH = os.environ.get('PERSISTENT_DISK_PATH') or os.path.join(BASE_DIR, 'uploads')

    # Dossier spécifique pour les images de produits
    UPLOAD_FOLDER = os.path.join(UPLOADS_BASE_PATH, 'products')
    
    # S'assure que ces dossiers existent au démarrage de l'app.
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
   
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pour le placeholder de WhatsApp
    WHATSAPP_NUMBER = "242065477443"
    
    # Configuration du cache (reste la même)
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
