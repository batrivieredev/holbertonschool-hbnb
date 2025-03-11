"""
Point d'entrée principal de l'application Flask.
Configure et initialise l'application avec ses extensions.

Extensions:
    - Flask-RESTx: API REST
    - Flask-SQLAlchemy: ORM
    - Flask-JWT: Authentification
    - Flask-Bcrypt: Hachage
"""

from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager  # ✅ Import du gestionnaire JWT
from app.extensions import db  # ✅ Import db depuis extensions
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns  # ✅ Import du namespace d'authentification
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt

# Initialisation du gestionnaire JWT
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    """Crée et configure l'instance de l'application Flask.

    Args:
        config_class (str): Classe de configuration à utiliser

    Configuration:
        - Base de données SQLite
        - JWT pour l'authentification
        - Documentation Swagger
    """
    app = Flask(__name__)

    # Configuration de l'application
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  # Changez pour production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # ✅ Clé secrète pour JWT (changez en production)

    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)  # ✅ Initialisation de JWTManager
    bcrypt.init_app(app)

    # Initialisation de l'API
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Enregistrement des namespaces
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')  # ✅ Ajout de l'authentification

    # Assurer la création des tables de la base de données
    with app.app_context():
        db.create_all()

    return app
