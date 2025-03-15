from flask import Flask
from app.extensions import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1 import api as api_v1

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Factory function to create the Flask application"""
    app = Flask(__name__)

    # Configuration
    app.config.from_object('config.DevelopmentConfig')

    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enregistrement de l'API RESTx
    api_v1.init_app(app)  # ✅ Au lieu de register_blueprint()

    return app
