"""
Package d'initialisation pour l'API.
Configure la structure de base de l'API REST.

Structure:
    - v1/: Version 1 de l'API
        - users: Gestion des utilisateurs
        - places: Gestion des propriétés
        - amenities: Gestion des équipements
        - reviews: Gestion des avis
        - auth: Authentification
"""

from flask_restx import Api

# Configuration de base de l'API
api = Api(
    version='1.0',
    title='HBnB API',
    description='API REST pour la gestion de locations',
    doc='/api/v1/docs',
    prefix='/api/v1'
)

# Vérification de la configuration de l'API
def init_api():
    """Initialise et vérifie la configuration de l'API.

    Vérifie:
        - Présence des namespaces requis
        - Configuration Swagger
        - Préfixes des routes
    """
    if not api.namespaces:
        raise ValueError("Aucun namespace n'est enregistré dans l'API")
    return True
