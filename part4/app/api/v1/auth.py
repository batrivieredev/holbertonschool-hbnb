from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app.extensions import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }), 200
    except Exception as e:
        print(f"Error in profile: {str(e)}")
        return jsonify({'message': 'Error retrieving profile'}), 500
    except Exception as e:
        print(f"Error in profile retrieval: {str(e)}")
        return jsonify({'message': 'Authentication error'}), 401
