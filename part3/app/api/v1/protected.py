from flask import jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('protected', description='Endpoints sécurisés')

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Un endpoint sécurisé nécessitant un JWT valide"""
        current_user = get_jwt_identity()  # Récupérer l'identité stockée dans le token
        return jsonify({'message': f'Bienvenue, utilisateur {current_user["id"]}!'})
