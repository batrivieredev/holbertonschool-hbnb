"""Application Flask pour HBNB"""
import os
from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt

def create_app():
    """Crée et configure l'application Flask"""
    app = Flask(__name__, static_folder='../static', static_url_path='')

    # Configuration
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(f'config.{env.capitalize()}Config')

    # Initialisation des extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # User loader pour JWT
    from app.models.user import User
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    # Blueprints
    from app.api.v1.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1')

    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    from app.api.v1.places import places_bp
    app.register_blueprint(places_bp, url_prefix='/api/v1')

    from app.api.v1.reviews import reviews_bp
    app.register_blueprint(reviews_bp, url_prefix='/api/v1')

    from app.api.v1.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    from app.api.v1.amenities import amenities_bp
    app.register_blueprint(amenities_bp, url_prefix='/api/v1')

    from app.api.v1.bookings import bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/api/v1')

    # Page d'accueil (servie statiquement)
    @app.route('/')
    def index():
        """Route pour la page d'accueil"""
        return app.send_static_file('index.html')

    # Pages statiques
    @app.route('/<path:path>')
    def static_files(path):
        """Route pour les fichiers statiques"""
        return app.send_static_file(path)

    return app
