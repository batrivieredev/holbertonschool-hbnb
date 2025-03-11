"""
Module d'initialisation de l'API REST.
Configure et enregistre les différents endpoints.

Structure:
    - users: Gestion des utilisateurs
    - amenities: Gestion des équipements
    - places: Gestion des lieux
    - reviews: Gestion des avis
    - auth: Authentification
"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app():
    """Crée et configure l'application Flask avec l'API REST.

    Configuration:
        - Version API: 1.0
        - Documentation Swagger intégrée
        - Namespaces préfixés avec /api/v1

    Returns:
        Flask: Application configurée avec tous les endpoints
    """
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API REST pour la gestion de locations',
        doc='/api/v1/docs'  # Point d'accès pour la documentation Swagger
    )

    # Enregistrement des namespaces avec leurs préfixes
    namespaces = [
        (amenities_ns, '/api/v1/amenities'),
        (users_ns, '/api/v1/users'),
        (places_ns, '/api/v1/places'),
        (reviews_ns, '/api/v1/reviews'),
        (auth_ns, '/api/v1/auth')
    ]

    for ns, path in namespaces:
        api.add_namespace(ns, path=path)

    return app
