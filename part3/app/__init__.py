"""
Point d'entrée principal de l'application Flask.
Configure et initialise l'application avec ses extensions.

Extensions:
    - Flask-RESTx: API REST
    - Flask-SQLAlchemy: ORM
    - Flask-JWT: Authentification
    - Flask-Bcrypt: Hachage
"""

import logging
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager  # ✅ Import du gestionnaire JWT
from app.extensions import db  # ✅ Import db depuis extensions
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns  # ✅ Import du namespace d'authentification
from app.api.v1.protected import api as protected_ns
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt

# Initialisation du gestionnaire JWT
jwt = JWTManager()
bcrypt = Bcrypt()

# Configuration du logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def create_app(config_class="config.DevelopmentConfig"):
    """Crée et configure l'instance de l'application Flask."""
    app = Flask(__name__)

    # Configuration de base
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'

    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Ajout d'une route de base pour vérifier que l'API fonctionne
    @app.route('/')
    def index():
        return {'message': 'Welcome to HBnB API'}, 200

    # Gestion des erreurs
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Internal server error'}, 500

    # Initialisation de l'API
    api = Api(app)

    # Enregistrement des namespaces
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

    # Création des tables
    with app.app_context():
        db.create_all()

    return app
