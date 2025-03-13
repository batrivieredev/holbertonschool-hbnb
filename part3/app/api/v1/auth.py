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

api = Namespace('auth', description='Operations d’authentification')

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l’utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l’utilisateur')
})

def admin_required(fn):
    """Vérifie si l'utilisateur est administrateur."""
    @wraps(fn)
    @jwt_required()  # ✅ Ajout de jwt_required() pour éviter une erreur 500
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()  # ✅ get_jwt_identity() retourne un dict
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper

@api.route('/login')
class Login(Resource):
    """Gère l'authentification des utilisateurs."""

    @api.expect(login_model)
    def post(self):
        """Authentification de l’utilisateur et génération du JWT token"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        print(f"📌 Tentative de connexion pour {email}")  # ✅ Debug

        # Récupérer l’utilisateur par email
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"📌 Mot de passe récupéré depuis la base : '{user.password}'")
        print(f"📌 Utilisateur trouvé en base : {user}")  # ✅ Debug
        print(f"📌 Mot de passe haché récupéré : {user.password}")

        # ⬇⬇ TEST MANUEL DE bcrypt ⬇⬇
        from flask_bcrypt import check_password_hash
        bcrypt_test = check_password_hash(user.password, password)
        print(f"✅ bcrypt_test (devrait être True) : {bcrypt_test}")  # ✅ Debug
        # ⬆⬆ FIN TEST ⬆⬆

        if not user or not user.verify_password(password):  # ✅ Vérification correcte
            print("❌ Identifiants invalides")  # ✅ Debug
            return {'error': 'Identifiants invalides'}, 401

        # Générer un token JWT
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        refresh_token = create_refresh_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@api.route('/refresh')
class TokenRefresh(Resource):
    """Permet de renouveler un token JWT."""

    @jwt_required(refresh=True)
    def post(self):
        """Générer un nouveau token JWT à partir d'un refresh token"""
        current_user = get_jwt_identity()  # ✅ get_jwt_identity() retourne un dict
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, 200
