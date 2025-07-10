# --- START OF FILE app.py ---

import os, csv, io, random, secrets
from datetime import datetime,timedelta
from flask import Flask, current_app, render_template, redirect, request, url_for, flash, request, send_file, abort, jsonify, session,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash # generate_password_hash est utilisé dans register et create-admin
from flask_wtf.csrf import CSRFProtect,generate_csrf
from urllib.parse import quote
from PIL import Image
#from flask_caching import Cache
from flask_migrate import Migrate

# Importer depuis les fichiers locaux
from config import Config
# Assurez-vous que ProductForm est bien celui que nous avons modifié dans forms.py
from forms import LoginForm, ProductForm, RegistrationForm, OrderForm
# Assurez-vous que Favorite est importé depuis models.py si vous l'y avez défini
from models import db, User, Product, TrafficLog, Order, Favorite # AJOUT DE Favorite
from sqlalchemy import func, distinct, or_,desc,cast
from collections import defaultdict
from markupsafe import Markup, escape # Pour le filtre nl2br
import click,json
#import pymysql
from sqlalchemy.orm import joinedload,aliased
#pymysql.install_as_MySQLdb()
from demo_data import new_demo_products_data

# Initialisation de l'application Flask
import sys # Assurez-vous que sys est importé en haut du fichier

# Logique pour déterminer les chemins des ressources, que ce soit en mode dev ou en mode exécutable
if getattr(sys, 'frozen', False):
    # Si l'application est "gelée" (exécutable PyInstaller)
    application_path = sys._MEIPASS
    template_dir = os.path.join(application_path, 'templates')
    static_dir = os.path.join(application_path, 'static')
    # Initialisation de l'application Flask avec des chemins explicites pour l'exécutable
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder=template_dir,
                static_folder=static_dir)
else:
    # Comportement normal en mode développement (python app.py)
    app = Flask(__name__, instance_relative_config=True)

#cache = Cache(app)
app.config.from_object(Config)

csrf = CSRFProtect(app)
migrate = Migrate(app, db)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=365)



# Initialisation des extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "info"



# --- FIN DE LA FONCTION MISE À JOUR ---

# Filtre nl2br (déjà présent)
@app.template_filter('nl2br')
def nl2br_filter(s):
    if not s:
        return ''
    s_escaped = escape(s)
    processed_s = str(s_escaped).replace('\r\n', '<br>\n').replace('\n', '<br>\n').replace('\r', '<br>\n')
    return Markup(processed_s)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def log_request_info():
    if current_user.is_authenticated and current_user.is_admin:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    if request.endpoint and 'static' not in request.endpoint:
        if current_user.is_authenticated and current_user.is_admin:
            pass
        else:
            product_id = request.view_args.get('product_id') if request.view_args else None
            ip_addr = request.remote_addr
            referrer = request.referrer if request.referrer else None
            utm_source_val = request.args.get('utm_source')
            utm_medium_val = request.args.get('utm_medium')
            utm_campaign_val = request.args.get('utm_campaign')
            utm_term_val = request.args.get('utm_term')
            utm_content_val = request.args.get('utm_content')

            log_entry = TrafficLog(
                user_id=current_user.id if current_user.is_authenticated else None,
                product_id=product_id,
                page_visited=request.path,
                ip_address=ip_addr,
                user_agent=request.user_agent.string,
                timestamp=datetime.utcnow(),
                # country_code a été retiré, si vous l'avez remis, décommentez
                # country_code = ...,
                referrer_url=referrer,
                utm_source=utm_source_val,
                utm_medium=utm_medium_val,
                utm_campaign=utm_campaign_val,
                utm_term=utm_term_val,
                utm_content=utm_content_val
            )
            db.session.add(log_entry)
            db.session.commit()

    if current_user.is_authenticated and not current_user.is_admin:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'config': app.config, 'url_for': url_for}

# --- FONCTION HELPER POUR LES FAVORIS (OPTIMISÉE) ---
def get_current_user_favorite_ids():
    """Helper pour obtenir les IDs des produits favoris de l'utilisateur actuel."""
    if current_user.is_authenticated and not current_user.is_admin:
        # OPTIMISATION: Utilise la nouvelle relation et ne charge que les IDs
        # C'est beaucoup plus rapide que de charger les objets Favorite entiers.
        fav_ids_tuples = current_user.favorites.with_entities(Favorite.product_id).all()
        return {id_tuple[0] for id_tuple in fav_ids_tuples} # Utiliser un set est encore plus rapide pour les vérifications
    return set() # Retourner un set vide

# --- Routes publiques ---
@app.route('/')
def index():
    # 1. On récupère les produits depuis la base de données
    featured_products = Product.query.order_by(Product.added_date.desc()).limit(10).all()

    # 2. ON TRAITE LES PRODUITS AVANT DE LES ENVOYER AU TEMPLATE (C'est la correction clé !)
    for product in featured_products:
        # On remplace le simple nom de fichier par l'URL complète générée par Flask
        product.image_file = url_for('serve_uploaded_file', path=f'products/{product.image_file}')

    # 3. On envoie maintenant la liste de produits traités à la page
    return render_template('index.html',
                           featured_products=featured_products, # Cette liste contient maintenant les bonnes URLs
                           favorite_product_ids=get_current_user_favorite_ids())

@app.route('/products')
#@cache.cached(timeout=3600)
def products_list():
    """
    MODIFIÉ: On passe à nouveau initial_query pour que le JS puisse le récupérer au premier chargement.
    """
    categories_list = [choice[0] for choice in ProductForm.category_choices if choice[0] != 'Non défini']
    genders_list = [choice[0] for choice in ProductForm.gender_choices]
    active_brands_tuples = db.session.query(Product.brand).filter(Product.brand.isnot(None), Product.brand != '').distinct().order_by(Product.brand).all()
    brands_list = [b[0] for b in active_brands_tuples]

    # On récupère TOUS les filtres initiaux depuis l'URL
    initial_query = request.args.get('query', '') # <-- RÉ-AJOUTÉ
    initial_category = request.args.get('category', 'all')
    initial_brand = request.args.get('brand', 'all')
    initial_gender = request.args.get('gender', 'all')

    return render_template('products.html',
                           categories=categories_list,
                           brands=brands_list,
                           genders=genders_list,
                           initial_query=initial_query, # <-- RÉ-AJOUTÉ
                           initial_category=initial_category,
                           initial_brand=initial_brand,
                           initial_gender=initial_gender
                           )

@app.route('/api/products_filter')
#@cache.cached(timeout=300, query_string=True)
def api_products_filter():
    """
    MODIFIÉ: L'URL de l'image pointe maintenant vers la nouvelle route 'serve_uploaded_file'.
    """
    page = request.args.get('page', 1, type=int)
    query_param = request.args.get('query', '', type=str)
    category_filter = request.args.get('category', 'all', type=str)
    brand_filter = request.args.get('brand', 'all', type=str)
    gender_filter = request.args.get('gender', 'all', type=str)
    per_page = 9

    products_query = Product.query.order_by(Product.added_date.desc())

    if query_param:
        products_query = products_query.filter(Product.name.ilike(f'%{query_param}%'))
    if category_filter != 'all' and category_filter:
        products_query = products_query.filter(Product.category == category_filter)
    if brand_filter != 'all' and brand_filter:
        products_query = products_query.filter(Product.brand == brand_filter)
    if gender_filter != 'all' and gender_filter:
        products_query = products_query.filter(Product.gender == gender_filter)

    try:
        products_pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    except Exception as e:
        app.logger.error(f"Erreur de pagination: {e}")
        return jsonify({'products': [], 'pagination': {'total_pages': 0, 'page': page, 'total_items': 0}}), 404

    user_favorite_ids = get_current_user_favorite_ids()

    products_data = []
    for product in products_pagination.items:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand or 'N/A',
            'price_info': product.price_info,
            # MODIFIÉ : Utilise la nouvelle route pour servir les images
            'image_file': url_for('serve_uploaded_file', path=f'products/{product.image_file}'),
            'detail_url': url_for('product_detail', product_id=product.id),
            'is_favorite': product.id in user_favorite_ids
        })

    return jsonify({
        'products': products_data,
        'pagination': {
            'page': products_pagination.page, 'per_page': products_pagination.per_page,
            'total_pages': products_pagination.pages, 'total_items': products_pagination.total,
            'has_prev': products_pagination.has_prev, 'has_next': products_pagination.has_next,
            'prev_num': products_pagination.prev_num if products_pagination.has_prev else None,
            'next_num': products_pagination.next_num if products_pagination.has_next else None
        }
    })

# --- NOUVELLE ROUTE À AJOUTER ---
@app.route('/api/filter_options')
#@cache.cached(timeout=300, query_string=True)
def api_filter_options():
    """
    NOUVEAU: Endpoint d'API pour obtenir les options de filtre dépendantes.
    Renvoie les marques disponibles pour une catégorie donnée (et à l'avenir, potentiellement d'autres options).
    """
    category = request.args.get('category', 'all', type=str)
    # On pourrait aussi ajouter un filtre par genre ici si besoin
    # gender = request.args.get('gender', 'all', type=str)

    # Requête de base pour les marques distinctes et non vides
    query = db.session.query(Product.brand).filter(Product.brand.isnot(None), Product.brand != '').distinct()

    # Si une catégorie spécifique est sélectionnée, on filtre les marques
    if category != 'all':
        query = query.filter(Product.category == category)

    # (Optionnel) Si on voulait aussi filtrer par genre:
    # if gender != 'all':
    #     query = query.filter(Product.gender == gender)

    # On trie les marques par ordre alphabétique pour une meilleure UX
    brands_tuples = query.order_by(Product.brand).all()
    brands_list = [b[0] for b in brands_tuples]

    return jsonify({'brands': brands_list})

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Affiche la page de détail d'un produit avec une logique de recommandation avancée.
    """
    product = Product.query.get_or_404(product_id)

    if not (current_user.is_authenticated and current_user.is_admin):
        product.views = (product.views or 0) + 1
        db.session.commit()

    product_page_url = url_for('product_detail', product_id=product.id, _external=True)
    product_image_url = url_for('serve_uploaded_file', path=f'products/{product.image_file}', _external=True)

    message_for_whatsapp = (
        f"Bonjour Luxury Akran,\n\n"
        f"Je suis intéressé(e) par le produit suivant :\n\n"
        f"*{product.name.strip()}*\n"
        f"Marque : {product.brand.strip() if product.brand else 'N/A'}\n\n"
        f"Vous pouvez voir la page du produit ici :\n{product_page_url}\n\n"
        f"Voici l'image pour référence :\n"
        f"{product_image_url}"
    )
    encoded_message = quote(message_for_whatsapp)
    whatsapp_link = f"https://wa.me/{current_app.config['WHATSAPP_NUMBER']}?text={encoded_message}"

    favorite_product_ids = []
    if current_user.is_authenticated and not current_user.is_admin:
        favorite_product_ids = [fav.product_id for fav in current_user.favorites]

    # --- LOGIQUE DE RECOMMANDATION HYBRIDE (AVANCÉE) ---
    target_genders = {'mixte'}
    if product.gender:
        target_genders.add(product.gender)

    recommended_ids = {product.id}
    recommended_products = []

    # 1. Priorité 1: Même catégorie, bon genre, plus vus
    recs_by_category = Product.query.filter(
        Product.category == product.category,
        Product.gender.in_(target_genders),
        Product.id != product.id
    ).order_by(Product.views.desc()).limit(10).all()
    for p in recs_by_category:
        if p.id not in recommended_ids:
            recommended_products.append(p)
            recommended_ids.add(p.id)

    # 2. Priorité 2: Même marque, bon genre, plus vus
    if len(recommended_products) < 10 and product.brand:
        needed = 10 - len(recommended_products)
        recs_by_brand = Product.query.filter(
            Product.brand == product.brand,
            Product.gender.in_(target_genders),
            Product.id.notin_(recommended_ids)
        ).order_by(Product.views.desc()).limit(needed).all()
        for p in recs_by_brand:
            if p.id not in recommended_ids:
                recommended_products.append(p)
                recommended_ids.add(p.id)

    # 3. Priorité 3: Même catégorie, bon genre, plus récents
    if len(recommended_products) < 10:
        needed = 10 - len(recommended_products)
        recs_by_date = Product.query.filter(
            Product.category == product.category,
            Product.gender.in_(target_genders),
            Product.id.notin_(recommended_ids)
        ).order_by(Product.added_date.desc()).limit(needed).all()
        for p in recs_by_date:
             if p.id not in recommended_ids:
                recommended_products.append(p)
                recommended_ids.add(p.id)

    # --- FIN DE LA LOGIQUE DE RECOMMANDATION ---

    # --- CORRECTION AJOUTÉE ICI ---
    # On parcourt la liste des produits recommandés pour créer une URL d'image valide pour chacun.
    # C'est cette étape qui manquait et qui causait le problème.
    for rec_product in recommended_products:
        rec_product.image_url = url_for('serve_uploaded_file', path=f'products/{rec_product.image_file}')

    # Rendu final du template avec toutes les données
    return render_template(
        'product_detail.html',
        product=product,
        whatsapp_link=whatsapp_link,
        favorite_product_ids=favorite_product_ids,
        recommended_products=recommended_products, # Chaque produit a maintenant un attribut 'image_url'
        title=f"{product.name} - Luxury Akran"
    )
# --- DANS app.py ---

# --- NOUVELLE ROUTE POUR SERVIR LES IMAGES DEPUIS LE DISQUE PERSISTANT (CORRIGÉE) ---
@app.route('/uploads/<path:path>')
def serve_uploaded_file(path):
    """
    Sert les fichiers depuis le dossier de base des uploads configuré dans config.py.
    Ceci est nécessaire car le dossier d'upload est maintenant en dehors de 'static'.
    Le chemin inclut des sous-dossiers comme 'products/image.jpg'.
    """
    base_path = current_app.config['UPLOADS_BASE_PATH']
    return send_from_directory(base_path, path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    # Afficher un message spécifique si la redirection est due aux favoris
    if request.method == 'GET' and request.args.get('reason') == 'favorites':
        # Vérifier si ce message spécifique n'est pas déjà dans les messages flash pour éviter les doublons
        flashes = session.get('_flashes', [])
        if not any(message_text == "Vous devez être connecté pour ajouter un produit à vos favoris." for category, message_text in flashes):
            flash("Vous devez être connecté pour ajouter un produit à vos favoris.", "info")

    if form.validate_on_submit():
        user = User.query.filter((User.email == form.email.data.lower()) | (User.username == form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # Tentative de suppression du message spécifique aux favoris s'il est présent,
            # pour ne pas qu'il s'affiche avec le message de succès.
            if '_flashes' in session:
                session['_flashes'] = [(cat, msg) for cat, msg in session.get('_flashes', []) if msg != "Vous devez être connecté pour ajouter un produit à vos favoris."]

            flash('Connexion réussie!', 'success') # Message de succès normal
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Échec de la connexion. Vérifiez email/nom d\'utilisateur et mot de passe.', 'danger')

    return render_template('login.html', title='Connexion', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            country=form.country.data,
            is_admin=False
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erreur lors de la création du compte : {e}")
            flash("Une erreur s'est produite lors de la création de votre compte. Veuillez réessayer.", "danger")
    return render_template('register.html', title='Créer un Compte', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

@app.route('/order/product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)
    form = OrderForm()

    if request.method == 'GET':
        form.product_name.data = product.name
        form.price_info.data = product.price_info
        if current_user.is_authenticated:
            form.customer_name.data = form.customer_name.data or current_user.username
            form.customer_email.data = form.customer_email.data or current_user.email

    if form.validate_on_submit():
        order = Order(
            product_id=product.id,
            price_info=form.price_info.data,
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            customer_address=form.customer_address.data,
            quantity=form.quantity.data,
            notes=form.notes.data
        )
        db.session.add(order)
        db.session.commit()
        flash(f'Votre commande pour "{product.name}" a été passée avec succès! Nous vous contacterons bientôt.', 'success')
        return redirect(url_for('product_detail', product_id=product.id))

    return render_template('place_order.html', title=f'Commander: {product.name}', form=form, product=product)


# --- ROUTES POUR LES FAVORIS ---
@app.route('/toggle_favorite/<int:product_id>', methods=['POST'])
@login_required
def toggle_favorite(product_id):
    if current_user.is_admin:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # AJAX
            return jsonify({'status': 'error', 'message': 'Les administrateurs ne peuvent pas gérer les favoris.'}), 403
        flash("Les administrateurs ne peuvent pas gérer les favoris.", "warning")
        return redirect(request.referrer or url_for('index'))

    product = Product.query.get_or_404(product_id)
    message_text = ""
    is_now_favorited = False # Nouvel état après l'action

    if current_user.is_favorited(product):
        current_user.remove_from_favorites(product)
        message_text = f"'{product.name}' a été retiré de vos favoris."
        is_now_favorited = False
        message_category = 'info'
    else:
        current_user.add_to_favorites(product)
        message_text = f"'{product.name}' a été ajouté à vos favoris."
        is_now_favorited = True
        message_category = 'success'

    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # AJAX
        return jsonify({
            'status': 'success',
            'message': message_text,
            'is_favorited': is_now_favorited,
            'product_id': product_id # Utile pour identifier le bouton à mettre à jour côté client
        })
    else: # Requête non-AJAX (fallback, ou si JS est désactivé)
        flash(message_text, message_category)
        return redirect(request.referrer or url_for('index'))


@app.route('/my_favorites')
@login_required
def my_favorites():
    if current_user.is_admin:
        flash("Les administrateurs n'ont pas de section 'Mes Favoris'.", "warning")
        return redirect(url_for('admin_dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page = 9

    # OPTIMISATION: On reconstruit la requête pour obtenir les produits favoris
    # On joint Product et Favorite et on filtre par l'utilisateur actuel.
    favorite_products_query = Product.query.join(
        Favorite, Favorite.product_id == Product.id
    ).filter(
        Favorite.user_id == current_user.id
    ).order_by(
        Favorite.added_date.desc()
    )

    favorite_products_pagination = favorite_products_query.paginate(page=page, per_page=per_page, error_out=False)

    # --- DÉBUT DE LA CORRECTION : PRÉPARER LES URLS D'IMAGE POUR LE TEMPLATE ---
    products_for_template = []
    for product in favorite_products_pagination.items:
        # Assurez-vous que l'image_file est traitée pour obtenir l'URL complète
        # Créer un nouvel attribut 'image_url' pour ne pas modifier l'objet SQLAlchemy original
        product.image_url = url_for('serve_uploaded_file', path=f'products/{product.image_file}')
        products_for_template.append(product)
    # --- FIN DE LA CORRECTION ---

    # Pour _product_card.html, tous les produits ici sont des favoris.
    # On peut simplement passer les IDs pour être cohérent.
    current_favorite_ids = {p.id for p in favorite_products_pagination.items}

    return render_template('my_favorites.html',
                           title="Mes Favoris",
                           products_pagination=favorite_products_pagination,
                           products=products_for_template, # Passez la liste de produits avec les URLs d'image corrigées
                           favorite_product_ids=current_favorite_ids)
    
# --- Fonctions et routes Admin ---
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Vous n'avez pas les droits d'accès à cette page.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__ # Important pour Flask
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    # On récupère le terme de recherche et la page depuis l'URL
    search_query = request.args.get('search_query', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10 # Nombre de produits par page pour le tableau admin
    # NOUVEAU : Récupérer la position de défilement depuis l'URL
    scroll_pos = request.args.get('scroll_pos', 0, type=int)


    # --- Statistiques rapides (déjà optimisées) ---
    total_products = db.session.query(Product.id).count()
    total_users = db.session.query(User.id).count()
    home_page_views = db.session.query(TrafficLog.id).filter_by(page_visited='/').count()
    total_orders = db.session.query(Order.id).count() # Renommé pour correspondre au template

    # --- Top 10 produits commandés ---
    top_ordered_products = db.session.query(
        Product, func.count(Order.id).label('order_count')
    ).join(Order, Product.id == Order.product_id)\
     .group_by(Product.id)\
     .order_by(func.count(Order.id).desc())\
     .limit(10).all()

    # --- Top 5 produits vus ---
    most_viewed_products = Product.query.filter(Product.views > 0).order_by(Product.views.desc()).limit(10).all()

    # --- Requête principale pour la LISTE PAGINÉE des produits ---
    order_count_subquery = db.session.query(
        Order.product_id, func.count(Order.id).label('order_count')
    ).group_by(Order.product_id).subquery()

    oc_alias = aliased(order_count_subquery)

    # On commence la requête de base
    query = db.session.query(
        Product, func.coalesce(oc_alias.c.order_count, 0).label('display_order_count')
    ).outerjoin(
        oc_alias, Product.id == oc_alias.c.product_id
    )

    # On applique le filtre de recherche si un terme a été fourni (SERVER-SIDE)
    if search_query:
        search_term = f'%{search_query}%'
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.category.ilike(search_term)
            )
        )

    # On trie et on applique la pagination
    products_pagination = query.order_by(Product.added_date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # --- On passe toutes les données au template ---
    return render_template('admin_dashboard.html',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users,
                           home_page_views=home_page_views,
                           top_ordered_products=top_ordered_products,
                           most_viewed_products=most_viewed_products,
                           products_pagination=products_pagination, # Passer l'objet pagination
                           products=products_pagination.items,  # Passer les éléments de la page actuelle
                           search_query=search_query,
                           scroll_pos=scroll_pos) # NOUVEAU : Passer la position de défilement au template

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = 'default_product.webp'  # Image par défaut

        # --- DÉBUT DE LA LOGIQUE D'UPLOAD MISE À JOUR ---
        if form.image_file.data:
            image_data = form.image_file.data
            if allowed_file(image_data.filename):
                # 1. Crée un nom de fichier unique et sécurisé
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(image_data.filename)
                filename = random_hex + f_ext

                # 2. Définit le chemin complet pour la sauvegarde
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                # 3. Redimensionne, compresse et sauvegarde l'image optimisée
                output_size = (1000, 1000)  # Taille maximale en pixels
                i = Image.open(image_data)
                i.thumbnail(output_size)  # Garde les proportions
                i.save(upload_path, optimize=True, quality=85) # Sauvegarde optimisée

            else:
                flash("Type de fichier image non autorisé.", "warning")
                return render_template('add_product.html', title='Ajouter Produit', form=form, legend='Ajouter Produit')
        # --- FIN DE LA LOGIQUE D'UPLOAD MISE À JOUR ---

        product = Product(
            name=form.name.data, brand=form.brand.data, description=form.description.data,
            price_info=form.price_info.data, image_file=filename,
            tags=form.tags.data, category=form.category.data, gender=form.gender.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_product.html', title='Ajouter Produit', form=form, legend='Ajouter Produit')

@app.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """
    MODIFIÉ: L'URL de l'image actuelle pointe vers 'serve_uploaded_file'.
    """
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.brand = form.brand.data
        product.description = form.description.data
        product.price_info = form.price_info.data
        product.tags = form.tags.data
        product.category = form.category.data
        product.gender = form.gender.data

        image_data = form.image_file.data

        if image_data and hasattr(image_data, 'filename'):
            if allowed_file(image_data.filename):
                if product.image_file and product.image_file != 'default_product.webp':
                    try:
                        # Le chemin de suppression est correct car il utilise UPLOAD_FOLDER de la config
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_file))
                    except OSError:
                        pass

                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(image_data.filename)
                filename = random_hex + f_ext
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                output_size = (1000, 1000)
                i = Image.open(image_data)
                i.thumbnail(output_size)
                i.save(upload_path, optimize=True, quality=85)

                product.image_file = filename
            else:
                flash("Type de fichier image non autorisé. L'image n'a pas été mise à jour.", "warning")

        db.session.commit()
        flash('Produit mis à jour avec succès!', 'success')
        return redirect(url_for('admin_dashboard'))

    # MODIFIÉ : Utilise la nouvelle route pour afficher l'image actuelle sur la page d'édition
    current_image = url_for('serve_uploaded_file', path=f'products/{product.image_file}')
    return render_template('add_product.html', title='Modifier Produit', form=form, legend=f'Modifier: {product.name}', current_image=current_image)

@app.route('/admin/product/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # NOUVEAU : Récupérer la position de défilement pour la redirection
    scroll_pos = request.form.get('scroll_pos', 0, type=int)

    # Étape 1 : Supprimer le fichier image associé (ça, ça ne change pas)
    if product.image_file and product.image_file != 'default_product.webp':
        try:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_file)
            if os.path.exists(image_path):
                os.remove(image_path)
        except OSError as e:
            # On affiche une erreur au cas où, mais on ne bloque pas la suppression
            flash(f"Erreur lors de la suppression de l'image : {e}", "warning")
            
    # Étape 2 : Supprimer l'objet produit de la session
    # La base de données s'occupera de supprimer en cascade les TrafficLog, Orders et Favorites liés.
    db.session.delete(product)
    
    # Étape 3 : Valider la transaction
    db.session.commit()
    
    flash('Produit et toutes ses données associées ont été supprimés avec succès!', 'success')
    # NOUVEAU : Ajouter scroll_pos à la redirection
    return redirect(url_for('admin_dashboard', scroll_pos=scroll_pos))

# --- NOUVELLE ROUTE POUR LA SUPPRESSION EN MASSE ---
@app.route('/admin/product/batch_delete', methods=['POST'])
@admin_required
def batch_delete_products():
    product_ids_to_delete = request.form.getlist('product_ids[]') # Récupère la liste des IDs cochés
    # NOUVEAU : Récupérer la position de défilement pour la redirection
    scroll_pos = request.form.get('scroll_pos', 0, type=int)

    deleted_count = 0
    errors = 0

    if not product_ids_to_delete:
        flash("Aucun produit sélectionné pour la suppression.", "warning")
        return redirect(url_for('admin_dashboard', scroll_pos=scroll_pos))

    for product_id in product_ids_to_delete:
        try:
            product = Product.query.get(product_id)
            if product:
                # Supprimer le fichier image associé
                if product.image_file and product.image_file != 'default_product.webp':
                    try:
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_file)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    except OSError as e:
                        app.logger.error(f"Erreur lors de la suppression de l'image {product.image_file}: {e}")
                        # On ne flashe pas pour chaque erreur d'image individuelle
                        pass # Continuer à supprimer l'entrée DB même si l'image persiste

                db.session.delete(product)
                deleted_count += 1
            else:
                errors += 1
                app.logger.warning(f"Produit avec ID {product_id} non trouvé pour la suppression en masse.")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erreur lors de la suppression du produit {product_id}: {e}")
            flash(f"Une erreur est survenue lors de la suppression de certains produits. Annulation de l'opération.", "danger")
            return redirect(url_for('admin_dashboard', scroll_pos=scroll_pos))

    db.session.commit() # Commit une seule fois après toutes les suppressions

    if deleted_count > 0:
        flash(f"{deleted_count} produit(s) supprimé(s) avec succès.", "success")
    if errors > 0:
        flash(f"Attention : {errors} produit(s) n'ont pas pu être trouvés ou supprimés.", "warning")

    return redirect(url_for('admin_dashboard', scroll_pos=scroll_pos))


# --- AJOUTS DANS app.py (DANS LA SECTION ADMIN) ---

@app.route('/admin/download_csv_template')
@admin_required
def download_csv_template():
    """
    Fournit un modèle CSV téléchargeable pour l'upload en masse.
    """
    # Crée un fichier en mémoire
    proxy = io.StringIO()
    # Colonnes attendues dans le CSV
    fieldnames = ['name', 'brand', 'description', 'price_info', 'tags', 'category', 'gender']
    writer = csv.writer(proxy)
    # Écrit l'en-tête (header)
    writer.writerow(fieldnames)

    # Prépare la réponse pour le téléchargement
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        download_name='template_produits.csv',
        mimetype='text/csv'
    )

@app.route('/admin/product/batch_upload', methods=['GET', 'POST'])
@admin_required
def batch_upload():
    """
    Gère l'upload en masse de produits via un fichier CSV et des images.
    """
    if request.method == 'POST':
        csv_file = request.files.get('csv_file')
        image_files = request.files.getlist('image_files')

        # --- Validations initiales ---
        if not csv_file or not image_files:
            flash("Veuillez fournir à la fois un fichier CSV et au moins un fichier image.", "danger")
            return redirect(url_for('batch_upload'))

        if not csv_file.filename.endswith('.csv'):
            flash("Le fichier de données doit être au format CSV.", "danger")
            return redirect(url_for('batch_upload'))

        try:
            # --- Lecture et traitement du CSV ---
            # Lire le contenu du fichier CSV en mémoire
            stream = io.StringIO(csv_file.stream.read().decode("UTF-8"), newline=None)
            csv_reader = csv.DictReader(stream)
            product_data_list = list(csv_reader)

            # --- Validation cruciale : correspondance du nombre d'éléments ---
            if len(product_data_list) != len(image_files):
                flash(f"Erreur : Le nombre de produits dans le CSV ({len(product_data_list)}) ne correspond pas au nombre d'images ({len(image_files)}).", "danger")
                return redirect(url_for('batch_upload'))

            products_added = 0
            # --- Boucle pour créer chaque produit ---
            for product_data, image_file in zip(product_data_list, image_files):
                if image_file and allowed_file(image_file.filename):
                    # Logique de traitement d'image (reprise de add_product)
                    random_hex = secrets.token_hex(8)
                    _, f_ext = os.path.splitext(image_file.filename)
                    filename = random_hex + f_ext
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    output_size = (1000, 1000)
                    i = Image.open(image_file)
                    i.thumbnail(output_size)
                    i.save(upload_path, optimize=True, quality=85)

                    # Création de l'objet Product
                    product = Product(
                        name=product_data.get('name', 'Produit sans nom'),
                        brand=product_data.get('brand'),
                        description=product_data.get('description'),
                        price_info=product_data.get('price_info', 'Contacter pour prix'),
                        tags=product_data.get('tags'),
                        category=product_data.get('category', 'Non défini'),
                        gender=product_data.get('gender', 'mixte'),
                        image_file=filename # Image associée
                    )
                    db.session.add(product)
                    products_added += 1
                else:
                    # Si un fichier n'est pas une image autorisée, on arrête tout
                    flash(f"Le fichier '{image_file.filename}' n'est pas un type d'image autorisé. L'opération a été annulée.", "warning")
                    db.session.rollback() # Annule les ajouts précédents
                    return redirect(url_for('batch_upload'))

            db.session.commit()
            flash(f"{products_added} produits ont été ajoutés avec succès !", "success")
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erreur lors de l'upload en masse : {e}")
            flash(f"Une erreur est survenue lors du traitement. Vérifiez le format de votre fichier CSV. Erreur: {e}", "danger")
            return redirect(url_for('batch_upload'))

    return render_template('batch_upload.html', title="Ajout en Masse de Produits")


# --- Commandes CLI ---
@app.cli.command("init-db")
@click.option('--recreate', is_flag=True, help='Supprime la base de données existante avant de créer (DANGER: perte de données).')
def init_db_command(recreate):
    """Initialise la base de données SQLite."""
    db_path = os.path.join(app.instance_path, app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])

    if recreate:
        if click.confirm(f'ATTENTION: Cela va supprimer le fichier de base de données existant ({db_path}). Êtes-vous sûr ?', abort=True):
            click.echo('Suppression de la base de données SQLite existente...')
            if os.path.exists(db_path):
                os.remove(db_path)
            # db.drop_all() n'est pas toujours fiable pour supprimer le fichier lui-même, la suppression directe est mieux.
            click.echo('Base de données SQLite supprimée.')

    if os.path.exists(db_path):
        click.echo(f"Le fichier de base de données '{db_path}' existe déjà. Utiliser --recreate pour le remplacer.")
        return

    click.echo('Création des tables dans la base de données SQLite...')
    # create_all ne fonctionne que dans un contexte d'application
    with app.app_context():
        db.create_all()
    click.echo('Tables créées avec succès.')
    click.echo(f"Base de données initialisée ici : {db_path}")

@app.cli.command("create-admin")
def create_admin_command():
    username = input("Entrez le nom d'utilisateur de l'admin: ")
    email = input("Entrez l'email de l'admin: ")
    password = input("Entrez le mot de passe de l'admin: ")

    with app.app_context(): # Bonne pratique d'envelopper les commandes dans un contexte d'app
        if User.query.filter((User.email == email.lower()) | (User.username == username)).first():
            print("Un utilisateur avec cet email ou nom d'utilisateur existe déjà.")
            return
        admin_user = User(username=username, email=email.lower(), is_admin=True)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
    print(f"Utilisateur admin '{username}' créé avec succès.")


@app.cli.command("populate-new-data")
@click.option('--confirm', is_flag=True, help='Confirmer avant d\'ajouter les données si des produits existent déjà.')
def populate_new_data_command(confirm):
    """Peuple la base de données avec un nouvel ensemble de produits inspirés par les images fournies."""
    if Product.query.first():
        click.echo("Attention : La base de données contient déjà des produits.", err=True)
        if confirm:
            if not click.confirm('Voulez-vous quand même ajouter les nouveaux produits de démonstration ? (Cela peut créer des doublons si les noms sont identiques)', abort=False):
                click.echo("Opération annulée par l'utilisateur.")
                return
        else:
            click.echo("Opération annulée. Utilisez --confirm pour ajouter les données malgré tout.")
            return

    count_added = 0
    for p_data in new_demo_products_data: # Utilise la liste globale
        existing_product = Product.query.filter_by(image_file=p_data['image_file']).first()
        if existing_product:
            click.echo(f"Produit avec image '{p_data['image_file']}' existe déjà. Ignoré.", color='yellow')
            continue

        product = Product(
            name=p_data.get('name', 'Produit sans nom'),
            brand=p_data.get('brand'),
            description=p_data.get('description'),
            price_info=p_data.get('price_info', 'Contacter pour prix'),
            image_file=p_data['image_file'],
            tags=p_data.get('tags'),
            category=p_data.get('category', 'Non défini'),
            gender=p_data.get('gender', 'mixte')
        )
        db.session.add(product)
        count_added += 1

    try:
        db.session.commit()
        click.echo(f"{count_added} nouveaux produits ajoutés avec succès à la base de données.", color='green')
    except Exception as e:
        db.session.rollback()
        click.echo(f"Erreur lors de l'ajout des produits : {e}", err=True, color='red')



if __name__ == '__main__':
    app.run(port=5008, debug=True)
