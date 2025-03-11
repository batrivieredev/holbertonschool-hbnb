"""
Module d'authentification de l'API.
Gère les tokens JWT et la sécurité des routes.

Fonctionnalités:
    - Login/Logout des utilisateurs
    - Génération de tokens JWT
    - Rafraîchissement des tokens
    - Protection des routes
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models import User  # Import du modèle utilisateur

api = Namespace('auth', description='Operations d’authentification')

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l’utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l’utilisateur')
})

@api.route('/login')
class Login(Resource):
    """Gère l'authentification des utilisateurs.

    Sécurité:
        - Validation des identifiants
        - Génération de token JWT
        - Durée de vie configurable
    """
    @api.expect(login_model)
    def post(self):
        """Authentification de l’utilisateur et génération du JWT token"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Récupérer l’utilisateur par email
        user = User.query.filter_by(email=email).first()

        # Vérifier si l’utilisateur existe et si le mot de passe est correct
        if not user or not check_password_hash(user.password, password):
            return {'error': 'Identifiants invalides'}, 401

        # Générer un token JWT
        access_token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin})

        return {'access_token': access_token}, 200
