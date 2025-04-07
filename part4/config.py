import os

class Config:
    """Configuration de base commune à tous les environnements."""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    RATE_LIMITING = True
    MAX_REQUESTS = 100
    CACHE_TYPE = "simple"

class DevelopmentConfig(Config):
    """Configuration spécifique à l'environnement de développement."""
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hbnb.db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwtkey")
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
