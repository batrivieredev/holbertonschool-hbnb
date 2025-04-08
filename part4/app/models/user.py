"""Module de gestion des utilisateurs."""
from app.extensions import db, bcrypt
from app.models.BaseModel import BaseModel
import re

class User(BaseModel):
    """Modèle pour les utilisateurs."""

    # Définition des colonnes
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def validate(self):
        """Valide les données de l'utilisateur."""
        # Validation de l'email
        if not self.email:
            raise ValueError("L'email est requis")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Format d'email invalide")

        # Validation du nom et prénom
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("Le prénom est requis et doit faire moins de 50 caractères")

        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Le nom est requis et doit faire moins de 50 caractères")

    def hash_password(self, password):
        """Hash le mot de passe de l'utilisateur."""
        if not password:
            raise ValueError("Le mot de passe est requis")
        if len(password) < 8:
            raise ValueError("Le mot de passe doit faire au moins 8 caractères")

        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Vérifie le mot de passe de l'utilisateur."""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def promote_to_admin(self):
        """Promeut l'utilisateur en administrateur."""
        self.is_admin = True
        self.save()

    def demote_from_admin(self):
        """Rétrograde l'administrateur en utilisateur normal."""
        self.is_admin = False
        self.save()

    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_user(data):
        """Crée un nouvel utilisateur."""
        if not data.get('password'):
            raise ValueError("Le mot de passe est requis")

        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_admin=data.get('is_admin', False)
        )
        user.hash_password(data['password'])
        user.validate()
        user.save()
        return user

    def update_from_dict(self, data):
        """Met à jour l'utilisateur à partir d'un dictionnaire."""
        if 'email' in data:
            self.email = data['email']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'password' in data:
            self.hash_password(data['password'])
        if 'is_admin' in data:
            self.is_admin = data['is_admin']

        self.validate()
        self.save()

    def __repr__(self):
        """Représentation textuelle de l'utilisateur."""
        return f'<User {self.email}>'
