"""
Module d'administration de l'API.
Fournit les endpoints réservés aux administrateurs.

Fonctionnalités:
    - Gestion des utilisateurs
    - Supervision du système
    - Configuration de l'application
    - Rapports et statistiques
"""

from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from api.v1.decorators import admin_required
from app.services.UsersFacade import UsersFacade


api = Namespace('admin', description='Endpoints réservés aux admins')
facade = UsersFacade()

@api.route('/dashboard')
class AdminDashboard(Resource):
    """Interface d'administration principale.

    Sécurité:
        - Authentification JWT requise
        - Droits administrateur requis
        - Journalisation des actions
    """
    @api.doc(security='jwt')
    @jwt_required()
    @admin_required
    def get(self):
        """Tableau de bord réservé aux administrateurs"""
        return {'message': 'Bienvenue dans le dashboard admin!'}

@api.route('/users')
class AdminUserList(Resource):
    @api.doc(security='jwt')
    @jwt_required()
    @admin_required
    def get(self):
        """Retrieve all users (Admin only)"""
        return [user.to_dict() for user in facade.get_all_users()], 200
