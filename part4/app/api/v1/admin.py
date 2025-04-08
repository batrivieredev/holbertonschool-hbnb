from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
import traceback

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Check if current user is admin
        if not current_user or not current_user.is_admin:
            return jsonify({"message": "Unauthorized. Admin privileges required."}), 403

        # Get request data
        data = request.get_json()
        if not data or not all(k in data for k in ['first_name', 'last_name', 'email', 'password', 'is_admin']):
            return jsonify({"message": "Missing required fields"}), 400

        # Check if user with email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "User with this email already exists"}), 400

        # Create new user
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            is_admin=data['is_admin']
        )
        new_user.hash_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_dict()
        }), 201
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        print(traceback.format_exc())
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the user"}), 500

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Check if current user is admin
        if not current_user or not current_user.is_admin:
            return jsonify({"message": "Unauthorized. Admin privileges required."}), 403

        # Get all users
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        print(f"Error listing users: {str(e)}")
        return jsonify({"message": "An error occurred while fetching users"}), 500

@admin_bp.route('/admin/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        # Check if current user is admin
        if not current_user or not current_user.is_admin:
            return jsonify({"message": "Unauthorized. Admin privileges required."}), 403

        # Get user to delete
        user_to_delete = User.query.get(user_id)
        if not user_to_delete:
            return jsonify({"message": "User not found"}), 404

        # Prevent self-deletion
        if user_to_delete.id == current_user.id:
            return jsonify({"message": "Cannot delete your own account"}), 400

        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the user"}), 500
