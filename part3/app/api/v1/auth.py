"""Module d'authentification et de contrôle d'accès."""

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from flask_bcrypt import check_password_hash  # ✅ Ajout pour SQLite
from app.models import User  # Import du modèle utilisateur
from functools import wraps
from app.services.UsersFacade import UsersFacade

api = Namespace('auth', description='Operations d’authentification')
facade = UsersFacade()

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l’utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l’utilisateur')
})

def admin_required(fn):
    """Vérifie si l'utilisateur est administrateur."""
    @wraps(fn)
    @api.doc(security='jwt')
    @jwt_required()  # ✅ Ajout de jwt_required() pour éviter une erreur 500
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()  # ✅ get_jwt_identity() retourne un dict
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        user = facade.authenticate_user(credentials['email'], credentials['password'])  # ✅ Use authentication method

        if not user:
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
        return {"access_token": access_token}, 200


@api.route('/refresh')
class TokenRefresh(Resource):
    """Permet de renouveler un token JWT."""

    @jwt_required(refresh=True)
    def post(self):
        """Générer un nouveau token JWT à partir d'un refresh token"""
        current_user = get_jwt_identity()  # ✅ get_jwt_identity() retourne un dict
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, 200
