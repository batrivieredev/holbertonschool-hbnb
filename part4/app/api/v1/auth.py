"""Module de gestion de l'authentification"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from app.models.user import User
from app.extensions import db

# Création du blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Crée un nouvel utilisateur"""
    try:
        # Récupère les données du formulaire
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données manquantes'}), 400

        # Vérifie les champs requis
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400

        # Vérifie si l'email existe déjà
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Cet email est déjà utilisé'}), 409

        # Crée le nouvel utilisateur (toujours non admin)
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=False
        )
        user.hash_password(data['password'])

        # Sauvegarde l'utilisateur
        db.session.add(user)
        db.session.commit()

        # Crée le token JWT
        access_token = create_access_token(identity=user.id)

        # Retourne le token et les infos utilisateur
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Authentifie un utilisateur et retourne un token JWT"""
    try:
        # Récupère les données du formulaire
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données manquantes'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400

        # Vérifie les identifiants
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

        # Crée le token JWT
        access_token = create_access_token(identity=user.id)

        # Retourne le token et les infos utilisateur
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Retourne le profil de l'utilisateur connecté"""
    try:
        # Récupère l'ID de l'utilisateur depuis le token
        current_user_id = get_jwt_identity()

        # Récupère l'utilisateur
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Retourne les informations de l'utilisateur
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
