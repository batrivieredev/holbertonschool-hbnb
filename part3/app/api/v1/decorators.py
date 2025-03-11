from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def admin_required(fn):
    """Un décorateur pour restreindre l’accès aux administrateurs uniquement"""
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'error': 'Accès interdit'}), 403
        return fn(*args, **kwargs)
    return wrapper
