#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel
from flask_bcrypt import Bcrypt, generate_password_hash


"""
Modèle SQLAlchemy pour les utilisateurs.
Définit la structure de données et les méthodes des comptes.

Table: users
Relations:
    - places: Lieux possédés par l'utilisateur
    - reviews: Avis postés par l'utilisateur
"""

bcrypt = Bcrypt()

from app.extensions import db, bcrypt
from app.models.BaseModel import BaseModel

class User(BaseModel):
    """User Model with password hashing"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        """Hashes the password before storing it"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Checks if a password matches the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert User object to dictionary (without password)"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
