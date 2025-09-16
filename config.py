## --- START OF FILE config.py ---

import os

# Le BASE_DIR pointe vers le dossier racine de votre application# --- START OF FILE config.py ---

import os

# Le BASE_DIR pointe vers le dossier racine de votre application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clé secrète pour la sécurité des sessions Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete_tres_difficile_a_deviner'
    
    # --- CONFIGURATION DE LA BASE DE DONNÉES ---
    # Stratégie :
    # 1. Si l'app est sur Render, utiliser la variable d'environnement DATABASE_URL (connexion interne, rapide).
    # 2. SINON (si l'app est en local), se connecter à la base de Render via son URL EXTERNE.
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
         # Sur Render, on utilise la connexion interne
         SQLALCHEMY_DATABASE_URI = database_url.replace("postgres://", "postgresql://", 1)
    else:
         # En local, on utilise l'URL EXTERNE que vous avez fournie
         SQLALCHEMY_DATABASE_URI = 'postgresql://luxury_akran_db_user:P2G82F6Iivnm2N0VMx2tCpzdlj9lKTEo@dpg-d1j2mp7diees73cid2jg-a.frankfurt-postgres.render.com/luxury_akran_db'

    # Désactive une fonctionnalité de Flask-SQLAlchemy qui n'est plus nécessaire et consomme des ressources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOADS_BASE_PATH = os.environ.get('PERSISTENT_DISK_PATH') or os.path.join(BASE_DIR, 'uploads')

    # 2. On définit le dossier spécifique pour les images de produits à l'intérieur de ce chemin de base.
    #    Ceci est le chemin physique où les fichiers seront sauvegardés.
    UPLOAD_FOLDER = os.path.join(UPLOADS_BASE_PATH, 'products')
    
    # 3. On s'assure que ces dossiers existent au démarrage de l'app.
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
   
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pour le placeholder de WhatsApp
    WHATSAPP_NUMBER = "242065477443"
    
    # Type de cache. 'SimpleCache' est un cache en mémoire.
    CACHE_TYPE = 'SimpleCache'
    # Durée de vie par défaut pour les éléments du cache, en secondes
    CACHE_DEFAULT_TIMEOUT = 300

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
