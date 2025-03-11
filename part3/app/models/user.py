#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel
from flask_bcrypt import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__ = 'users'  # ✅ Define table name

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    def hash_password(self, password):
        """Hache et stocke le mot de passe."""
        self.password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe donné correspond au hash stocké."""
        return check_password_hash(self.password, password)
