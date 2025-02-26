from app.services.facade import HBnBFacade
from app.models.user import User


class UsersFacade(HBnBFacade):

    def __init__(self):
        super().__init__()

    def create_user(self, user_data):
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
