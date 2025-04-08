"""Module d'initialisation de l'application Flask"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from app.extensions import db, bcrypt, jwt
from app.api.v1 import api_v1

def create_app():
    """
    Crée et configure l'application Flask

    Returns:
        Flask: L'application configurée
    """
    # Création de l'application
    app = Flask(__name__, static_folder=None)  # Désactive le dossier static par défaut

    # Configuration
    app.config.from_object('config.DevelopmentConfig')

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # CORS - Autorise les requêtes cross-origin
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Authorization"],
            "supports_credentials": True
        }
    })

    # Initialisation de la base de données
    with app.app_context():
        db.create_all()

    # Enregistrement des blueprints
    app.register_blueprint(api_v1)

    # Gestionnaire des fichiers statiques
    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def serve_static(path):
        """Sert les fichiers statiques depuis le dossier /static"""
        static_folder = os.path.join(os.path.dirname(app.root_path), 'static')

        # Vérifie d'abord si le fichier existe dans un sous-dossier
        for subdir in ['css', 'js', 'images']:
            file_path = os.path.join(static_folder, subdir, path)
            if os.path.isfile(file_path):
                return send_from_directory(os.path.join(static_folder, subdir), path)

        # Si le fichier est directement dans /static
        if os.path.isfile(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)

        # Par défaut, retourne index.html
        return send_from_directory(static_folder, 'index.html')

    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found_error(error):
        """Gère les erreurs 404"""
        if "/api/" in error.description:
            return {'error': 'Not found'}, 404
        return send_from_directory(
            os.path.join(os.path.dirname(app.root_path), 'static'),
            'index.html'
        )

    return app
