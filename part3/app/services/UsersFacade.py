"""
Facade pour la gestion des utilisateurs.
Implémente la logique métier des comptes utilisateurs.

Responsabilités:
    - Validation des données utilisateur
    - Hachage des mots de passe
    - Gestion des sessions
    - Vérification des droits
"""

from app.models.user import User
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def is_valid_email(email):
    """Vérifie si l'email est valide avec une regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$'
    return re.match(email_regex, email) is not None

class UsersFacade():

    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)

    def create_user(self, user_data):
        email = user_data.get("email")
        password = user_data.get("password")

        if not is_valid_email(email):
            print("❌ Email invalide:", email)  # ✅ Debug email
            return None  # Rejette l'email invalide

        if not password:
            print("❌ Mot de passe manquant!")  # ✅ Debug password
            return None

        user_data["password"] = self.hash_password(password)
        print("✅ Création utilisateur avec email:", email)  # ✅ Debug utilisateur

        user = User(**user_data)
        self.user_repo.add(user)
        print(f"✅ Utilisateur {email} créé en base")
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        user = self.user_repo.get_by_attribute('email', email)
        return user if user else None

    def get_all_users(self):
        """Récupérer tous les utilisateurs."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.user_repo.update(user.id, user_data)
        return user

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    def hash_password(self, password):
        """Hache et retourne le mot de passe."""
        return bcrypt.generate_password_hash(password).decode('utf-8')  # ✅ Retourne la valeur hachée

    def verify_password(self, user, password):
        """Vérifie si le mot de passe fourni correspond.

        Sécurité:
            - Utilise bcrypt pour le hachage
            - Protection contre les attaques timing
            - Nombre d'itérations configurable

        Args:
            user (User): Utilisateur dont on vérifie le mot de passe
            password (str): Mot de passe en clair

        Returns:
            bool: True si valide, False sinon
        """
        return bcrypt.check_password_hash(user.password, password)  # ✅ Vérifie le hash du bon utilisateur