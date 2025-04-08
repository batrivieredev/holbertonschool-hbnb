"""Configuration de l'application Flask HBNB"""
import os
from datetime import timedelta

class Config:
    """Configuration de base avec les paramètres communs"""

    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # Clé secrète pour les sessions
    STATIC_FOLDER = 'static'  # Dossier des fichiers statiques

    # Configuration SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True  # Vérifie la connexion avant utilisation
    }

    # Configuration JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # Clé pour les tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Durée de validité du token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Durée du refresh token
    JWT_ERROR_MESSAGE_KEY = 'error'  # Clé pour les messages d'erreur

    # Configuration sécurité
    SESSION_COOKIE_SECURE = True  # Cookie sécurisé (HTTPS)
    SESSION_COOKIE_HTTPONLY = True  # Cookie accessible uniquement par HTTP
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protection CSRF
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Durée de session

    # Configuration CORS
    CORS_HEADERS = 'Content-Type'  # Headers autorisés pour CORS

class DevelopmentConfig(Config):
    """Configuration pour le développement"""

    DEBUG = True  # Active le mode debug
    TESTING = False
    ENV = 'development'

    # Base de données SQLite pour le développement
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb.db'

    # Désactive certaines sécurités en développement
    SESSION_COOKIE_SECURE = False

    # JWT plus long en développement
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class TestingConfig(Config):
    """Configuration pour les tests"""

    DEBUG = False
    TESTING = True
    ENV = 'testing'

    # Base de données en mémoire pour les tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Désactive CSRF pour les tests
    WTF_CSRF_ENABLED = False

    # JWT court pour les tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3)

class ProductionConfig(Config):
    """Configuration pour la production"""

    DEBUG = False
    TESTING = False
    ENV = 'production'

    # URL de la base de données depuis variable d'environnement
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb.db')

    # Sécurité renforcée en production
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    # JWT plus restrictif en production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    def __init__(self):
        """Valide la configuration de production"""
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key':
            raise ValueError("La clé secrète de production doit être définie")

        if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == 'jwt-secret-key':
            raise ValueError("La clé JWT de production doit être définie")

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
