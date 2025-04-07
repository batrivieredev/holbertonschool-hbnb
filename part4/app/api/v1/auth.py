from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
    }), 200

@auth_bp.route('/auth/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'message': 'Missing or invalid token'}), 401

    # Extract user ID from token and return user profile
    # This is a simplified version - you might want to add proper token validation
    try:
        user = User.query.get(token.split()[1])
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }), 200
    except Exception:
        return jsonify({'message': 'Invalid token'}), 401
