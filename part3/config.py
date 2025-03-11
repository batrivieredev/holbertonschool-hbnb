import os

"""
Configuration de l'application.
Définit les différents environnements (dev, prod, test).

Variables d'environnement:
    - SECRET_KEY: Clé secrète de l'application
    - JWT_SECRET_KEY: Clé pour les tokens JWT
    - DATABASE_URL: URL de la base de données
"""

class Config:
    """Configuration de base commune à tous les environnements."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuration spécifique à l'environnement de développement.

    Caractéristiques:
        - Mode debug activé
        - Base de données SQLite locale
        - Clés par défaut pour dev
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_super_secret_key")
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
