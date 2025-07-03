# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    # L'option ondelete='CASCADE' est une instruction au niveau de la base de données
    # pour garantir la suppression en cascade.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False, index=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    # back_populates est utilisé pour la relation bidirectionnelle avec User et Product
    user = db.relationship('User', back_populates='favorites')
    product = db.relationship('Product', back_populates='favorited_by')

    # Contrainte unique pour empêcher les doublons
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='_user_product_favorite_uc'),)

    def __repr__(self):
        return f'<Favorite User {self.user_id} -> Product {self.product_id}>'


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # === RELATIONS AVEC CASCADE ===
    # Supprime les commandes de l'utilisateur si l'utilisateur est supprimé.
    orders = db.relationship('Order', backref='customer', lazy='dynamic', cascade="all, delete-orphan")

    # Supprime les favoris de l'utilisateur si l'utilisateur est supprimé.
    favorites = db.relationship(
        'Favorite', 
        back_populates='user', 
        lazy='dynamic', 
        cascade='all, delete-orphan'
    )
    
    # Supprime les logs de trafic de l'utilisateur si l'utilisateur est supprimé.
    traffic_logs = db.relationship('TrafficLog', backref='user', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,  method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_favorited(self, product):
        return self.favorites.filter_by(product_id=product.id).first() is not None

    def add_to_favorites(self, product):
        if not self.is_favorited(product):
            fav = Favorite(user=self, product=product)
            db.session.add(fav)
            return True
        return False

    def remove_from_favorites(self, product):
        fav = self.favorites.filter_by(product_id=product.id).first()
        if fav:
            db.session.delete(fav)
            return True
        return False
        
    def __repr__(self):
        return f'<User {self.username} (Country: {self.country})>'
    
    @property
    def initials(self):
        if not self.username:
            return "?"
        return self.username[0].upper()


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    brand = db.Column(db.String(50), index=True)
    description = db.Column(db.Text)
    price_info = db.Column(db.String(100), default="Contacter pour prix")
    image_file = db.Column(db.String(100), nullable=False, default='default_product.jpg')
    tags = db.Column(db.String(200))
    category = db.Column(db.String(50), index=True)
    gender = db.Column(db.String(20), default="Unisexe", index=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    # === RELATIONS AVEC CASCADE ===
    # Supprime les entrées de favoris liées à ce produit s'il est supprimé.
    favorited_by = db.relationship(
        'Favorite', 
        back_populates='product', 
        lazy='dynamic', 
        cascade='all, delete-orphan'
    )

    # Supprime les logs de trafic liés à ce produit s'il est supprimé.
    traffic_logs = db.relationship('TrafficLog', backref='product', lazy='dynamic', cascade="all, delete-orphan")
    
    # Supprime les commandes liées à ce produit s'il est supprimé.
    orders = db.relationship('Order', backref='product', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name} (Cat: {self.category}, Gender: {self.gender})>'


class TrafficLog(db.Model):
    __tablename__ = 'traffic_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True, index=True)
    page_visited = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    referrer_url = db.Column(db.Text, nullable=True)
    utm_source = db.Column(db.String(100), nullable=True)
    utm_medium = db.Column(db.String(100), nullable=True)
    utm_campaign = db.Column(db.String(100), nullable=True)
    utm_term = db.Column(db.String(100), nullable=True)
    utm_content = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<TrafficLog {self.page_visited} by {self.user_id or self.ip_address}>'


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False, index=True)
    customer_phone = db.Column(db.String(30), nullable=True)
    customer_address = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_info = db.Column(db.String(100), nullable=True, default="Non spécifié")
    notes = db.Column(db.Text, nullable=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(50), default='Nouvelle', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Order {self.id} for Product {self.product_id} by {self.customer_name}>'