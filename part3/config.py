import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_super_secret_key")
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
