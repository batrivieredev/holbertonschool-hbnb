"""
Extensions Flask de l'application.
Définit les instances des extensions pour éviter les dépendances circulaires.

Extensions:
    - SQLAlchemy: ORM pour la base de données
    - JWT: Gestion des tokens d'authentification
    - Bcrypt: Hachage des mots de passe
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Instance SQLAlchemy partagée dans toute l'application
db = SQLAlchemy()  # Define it globally without app binding
bcrypt = Bcrypt()
jwt = JWTManager()
