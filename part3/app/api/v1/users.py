#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services.UsersFacade import UsersFacade, is_valid_email
from app.api.v1.auth import admin_required

"""
Module gérant l'API des utilisateurs.
Implémente les endpoints REST pour la gestion des comptes utilisateurs.

Routes:
    POST /users/ : Création d'un compte
    GET /users/ : Liste tous les utilisateurs
    GET /users/<id> : Détails d'un utilisateur
    PUT /users/<id> : Mise à jour d'un profil
"""

api = Namespace('users', description='User operations')

# Modèles pour validation des données
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom de l’utilisateur', example="John"),
    'last_name': fields.String(required=True, description='Nom de l’utilisateur', example="Doe"),
    'email': fields.String(required=True, description='Email unique', example="john.doe@example.com"),
    'password': fields.String(required=True, description='Mot de passe (sera haché)', example="password123")
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

facade = UsersFacade()  # Instance unique


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @jwt_required()
    @admin_required
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid email format')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Créer un nouvel utilisateur et générer un JWT."""
        user_data = api.payload
        print("📌 Données reçues par l'API:", user_data)  # ✅ Debug

        email = user_data.get('email')
        if not email or not is_valid_email(email):
            print("❌ Email invalide:", email)  # ✅ Debug
            return {'error': 'Invalid email format'}, 400

        existing_user = facade.get_user_by_email(email)
        if existing_user:
            print("❌ Email déjà utilisé:", email)  # ✅ Debug
            return {'error': 'Email already registered'}, 400

        password = user_data.get('password')
        if not password:
            print("❌ Mot de passe manquant!")  # ✅ Debug
            return {'error': 'Password is required'}, 400

        user_data['password'] = facade.hash_password(password)
        print("✅ Mot de passe haché:", user_data['password'])  # ✅ Debug

        new_user = facade.create_user(user_data)
        if not new_user:
            print("❌ Erreur lors de la création de l'utilisateur.")  # ✅ Debug
            return {'error': 'Invalid user data'}, 400

        access_token = create_access_token(identity={'id': new_user.id, 'is_admin': new_user.is_admin})
        refresh_token = create_refresh_token(identity={'id': new_user.id, 'is_admin': new_user.is_admin})

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201  # ✅ Doit retourner `201 Created`

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Récupérer la liste des utilisateurs."""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Récupérer un utilisateur par ID."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @admin_required
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized - Cannot modify other users')
    @api.response(403, 'Admin privileges required')
    def put(self, user_id):
        """Update user profile (self only)"""
        current_user = get_jwt_identity()

        if str(user_id) != str(current_user.get('id')):
            return {'error': 'Cannot modify other users information'}, 403

        # Empêcher la modification de l'email et du mot de passe
        user_data = api.payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'Cannot modify email or password'}, 400

        email = user_data.get("email")

        if email and not is_valid_email(email):
            return {'error': 'Invalid email format'}, 400

        if "password" in user_data:
            return {'error': 'Password update not allowed via this endpoint'}, 400

        user = facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found or invalid data'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
