from app.persistence.repository import InMemoryRepository
from app.services.UsersFacade import UsersFacade


class HBnBFacade(UsersFacade):
    def __init__(self):
        super().__init__()
        self.user_repo = UsersFacade()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
