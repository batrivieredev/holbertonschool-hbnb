from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.models import User  # Import du modèle utilisateur

api = Namespace('auth', description='Operations d’authentification')

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l’utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l’utilisateur')
})

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
        print(f"📌 Utilisateur trouvé en base : {user}")  # ✅ Debug

        # Vérifier si l’utilisateur existe et si le mot de passe est correct
        if not user or not user.verify_password(password):
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
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, 200
