from app.services.UsersFacade import UsersFacade
from app.services.AmenityFacade import AmenityFacade
from app.services.PlaceFacade import PlaceFacade
from app.services.ReviewFacade import ReviewFacade
from app.models.user import User


class HBnBFacade(UsersFacade, AmenityFacade):
    def __init__(self):
        super().__init__()
        self.user_repo = UsersFacade()
        self.place_repo = PlaceFacade()
        self.review_repo = ReviewFacade()
        self.amenity_repo = AmenityFacade()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()
