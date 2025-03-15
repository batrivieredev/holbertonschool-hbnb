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

from flask_restx import Api

# Import des namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

# Définition de l'objet API global
api = Api(
    version="1.0",
    title="HBnB API",
    description="API REST pour la gestion de locations",
    doc="/api/v1/docs",
)

# Ajout des namespaces
api.add_namespace(users_ns, path="/users")
api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
api.add_namespace(amenities_ns, path="/amenities")
api.add_namespace(auth_ns, path="/auth")
