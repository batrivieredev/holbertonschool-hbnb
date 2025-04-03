from flask import Flask
from app.extensions import db, bcrypt, jwt
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    """Factory function to create the Flask application"""
    app = Flask(__name__)

    # Configuration
    app.config.from_object('config.DevelopmentConfig')

    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configuration Swagger UI
    SWAGGER_URL = '/api/v1'  # URL pour accéder à Swagger UI
    API_URL = '/static/swagger.json'  # Emplacement du fichier swagger

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "HBNB API"
        }
    )

    # Enregistrement du blueprint Swagger
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # S'assurer que le dossier static existe
    if not os.path.exists(os.path.join(app.root_path, 'static')):
        os.makedirs(os.path.join(app.root_path, 'static'))

    # Import et enregistrement de l'API
    from app.api.v1 import api as api_v1
    api_v1.init_app(app)

    return app
