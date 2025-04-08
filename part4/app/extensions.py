"""Extensions Flask et fonctions d'initialisation"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

# Initialisation des extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Active le support des clés étrangères pour SQLite"""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def init_db_events():
    """Configure les événements de la base de données"""

    @event.listens_for(db.session, 'after_commit')
    def after_commit(session):
        """Actions à effectuer après un commit"""
        session.info.clear()

    @event.listens_for(db.session, 'after_rollback')
    def after_rollback(session):
        """Actions à effectuer après un rollback"""
        session.info.clear()

    @event.listens_for(db.session, 'after_soft_rollback')
    def after_soft_rollback(session, previous_transaction):
        """Actions à effectuer après un soft rollback"""
        session.info.clear()

@jwt.user_identity_loader
def user_identity_lookup(user_id):
    """Convertit l'identité de l'utilisateur pour le JWT"""
    return str(user_id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Charge l'utilisateur à partir du JWT"""
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

# Configuration des messages d'erreur JWT
jwt_messages = {
    'token_expired': 'Le token a expiré',
    'invalid_token': 'Token invalide',
    'unauthorized': 'Accès non autorisé',
    'token_revoked': 'Le token a été révoqué',
    'fresh_token_required': 'Un token fresh est requis',
    'jwt_decode_error': 'Erreur de décodage du token',
    'invalid_header': 'En-tête de token invalide',
    'revoked_token': 'Le token a été révoqué',
    'user_lookup_error': 'Erreur lors de la recherche de l\'utilisateur',
    'fresh_token_required': 'Un token fresh est requis',
    'invalid_audience': 'Audience invalide',
    'invalid_issuer': 'Émetteur invalide',
    'invalid_claim': 'Revendication invalide',
    'missing_claim': 'Revendication manquante',
    'invalid_header_padding': 'Padding d\'en-tête invalide'
}

# Application des messages d'erreur JWT
for error_key, message in jwt_messages.items():
    if hasattr(jwt, error_key + '_loader'):
        getattr(jwt, error_key + '_loader')(lambda: ({"msg": message}, 401))
