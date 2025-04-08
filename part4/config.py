import os

class Config:
    """Configuration de base commune à tous les environnements."""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hbnb.db")
    DEBUG = False
    RATE_LIMITING = True
    MAX_REQUESTS = 100
    CACHE_TYPE = "simple"

class DevelopmentConfig(Config):
    """Configuration spécifique à l'environnement de développement."""
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    # Store database in current directory
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hbnb.db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwtkey")
    JWT_ACCESS_TOKEN_EXPIRES = False  # For development only
    JWT_ERROR_MESSAGE_KEY = "message"
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
