from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from api.v1.decorators import admin_required

api = Namespace('admin', description='Endpoints réservés aux admins')

@api.route('/dashboard')
class AdminDashboard(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        """Tableau de bord réservé aux administrateurs"""
        return {'message': 'Bienvenue dans le dashboard admin!'}
