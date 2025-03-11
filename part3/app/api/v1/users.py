#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.UsersFacade import UsersFacade, is_valid_email

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
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur', example="John"),
    'last_name': fields.String(required=True, description='Nom de l\'utilisateur', example="Doe"),
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
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid email format')
    @api.response(400, 'Email already registered')
    def post(self):
        """Créer un nouvel utilisateur."""
        user_data = api.payload

        email = user_data.get('email')
        if not email or not is_valid_email(email):
            return {'error': 'Invalid email format'}, 400

        existing_user = facade.get_user_by_email(email)
        if existing_user:
            return {'error': 'Email already registered'}, 400

        password = user_data.get('password')
        if not password:
            return {'error': 'Password is required'}, 400

        hashed_password = facade.hash_password(password)
        user_data['password'] = hashed_password

        new_user = facade.create_user(user_data)
        if not new_user:
            return {'error': 'Invalid user data'}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

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

    @api.expect(user_update_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid email format')
    def put(self, user_id):
        """Mettre à jour un utilisateur."""
        user_data = api.payload
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
