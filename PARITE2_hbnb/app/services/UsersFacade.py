from app.models.user import User
from app.persistence.repository import InMemoryRepository
import re

def is_valid_email(email):
    """Vérifie si l'email est valide avec une regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$'
    return re.match(email_regex, email) is not None

class UsersFacade():

    _instance = None

    def __init__(self):
        self.user_repo = InMemoryRepository()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsersFacade, cls).__new__(cls)
            cls._instance.user_repo = InMemoryRepository()  # Garde le stockage en mémoire
        return cls._instance

    def create_user(self, user_data):
        email = user_data.get("email")

        if not is_valid_email(email):
            return None  # Rejette l'email invalide

        user = User(**user_data)
        self.user_repo.add(user)
        print(f"✅ Debug: User created {user.id}")
        return user

    def get_user(self, user_id):
        print(f"🔍 Debug: Searching for user ID {user_id} in user_repo")
        user = self.user_repo.get(user_id)
        print(f"🔍 Debug: get_user({user_id}) found {user}")  # Ajout du print pour vérifier
        return user

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
