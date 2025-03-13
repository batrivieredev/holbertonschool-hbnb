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

class User(BaseModel):
    """Représente un utilisateur dans la base de données.

    Attributs:
        first_name (str): Prénom
        last_name (str): Nom
        email (str): Email unique
        password (str): Mot de passe haché
        is_admin (bool): Statut administrateur

    Relations:
        places: Liste des lieux possédés
        reviews: Liste des avis postés

    Méthodes:
        hash_password: Hache un mot de passe
        verify_password: Vérifie un mot de passe
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Stocke le hash
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    def set_password(self, password):
        """Hache le mot de passe et l'enregistre"""
        from flask_bcrypt import generate_password_hash
        self.password = generate_password_hash(password).decode('utf-8')
        print(f"📌 DEBUG : Mot de passe haché dans `set_password()` -> {self.password}")  # ✅ Debug

    def verify_password(self, password):
        """Vérifie si un mot de passe correspond au hash stocké."""
        from flask_bcrypt import check_password_hash  # ✅ Import local pour éviter les problèmes
        verification = check_password_hash(self.password, password)

        print(f"📌 Debug bcrypt : password_clair='{password}', hash_stocké='{self.password}'")
        print(f"✅ Résultat de bcrypt : {verification}")  # ✅ True si correct, False si erreur

        return verification
