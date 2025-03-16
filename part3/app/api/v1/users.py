#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.UsersFacade import UsersFacade, is_valid_email
from app.api.v1.decorators import admin_required

"""
Module gérant l'API des utilisateurs.
Implémente les endpoints REST pour la gestion des comptes utilisateurs.

Routes:
    POST /users/ : Création d'un compte (OUVERT À TOUS)
    GET /users/ : Liste tous les utilisateurs (PUBLIC)
    GET /users/<id> : Détails d'un utilisateur (PUBLIC)
    PUT /users/<id> : Mise à jour d'un profil (UTILISATEUR CONNECTÉ)
"""

api = Namespace('users', description='User operations')

# Modèles pour validation des données
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="Prénom", example="John"),
    'last_name': fields.String(required=True, description="Nom", example="Doe"),
    'email': fields.String(required=True, description="Email unique", example="john.doe@example.com"),
    'password': fields.String(required=True, description="Mot de passe (sera haché)", example="password123")
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='Prénom'),
    'last_name': fields.String(description='Nom')
})

facade = UsersFacade()  # Instance unique

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid email format')
    @api.response(400, 'Email already registered')
    @admin_required
    @jwt_required()
    def post(self):
        """Créer un nouvel utilisateur (Inscription ouverte)"""
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

        # Hachage du mot de passe avant stockage
        user_data['password'] = facade.hash_password(password)
        print("✅ Mot de passe haché:", user_data['password'])  # ✅ Debug

        new_user = facade.create_user(user_data)
        if not new_user:
            print("❌ Erreur lors de la création de l'utilisateur.")  # ✅ Debug
            return {'error': 'Invalid user data'}, 400


        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201  # ✅ `201 Created` sans token JWT


    @api.response(200, 'List of users retrieved successfully')
    @jwt_required()  # ✅ Ajout de protection
    @admin_required  # ✅ Seuls les admins peuvent voir la liste des utilisateurs
    def get(self):
        """Récupérer la liste des utilisateurs (ADMIN ONLY)."""
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

    @api.doc(security='jwt')
    @jwt_required()
    @admin_required
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized - Cannot modify other users')
    def put(self, user_id):
        """Mettre à jour son propre profil (Nom et Prénom uniquement)"""
        current_user = get_jwt_identity()

        if str(user_id) != str(current_user.get('id')):
            return {'error': 'Unauthorized - You can only modify your own profile'}, 403

        user_data = api.payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'Cannot modify email or password'}, 400

        user = facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found or invalid data'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
