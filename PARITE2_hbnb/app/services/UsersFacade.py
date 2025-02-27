from app.models.user import User
from app.persistence.repository import InMemoryRepository
import re

def is_valid_email(email):
    """Vérifie si l'email est valide avec une regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

class UsersFacade():

    def __init__(self):
        self.user_repo = InMemoryRepository()


    def create_user(self, user_data):
        email = user_data.get("email")

        if not is_valid_email(email):
            return None  # Rejette l'email invalide

        user = User(**user_data)
        self.user_repo.add(user)
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
