from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade():
    def __init__(self):
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            self.amenity_repo.update(amenity)
        return amenity

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)
