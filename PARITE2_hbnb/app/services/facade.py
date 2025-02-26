from app.persistence.repository import InMemoryRepository
from abc import ABC, abstractmethod

class HBnBFacade(ABC):
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    @abstractmethod
    def create_user(self, user_data):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass