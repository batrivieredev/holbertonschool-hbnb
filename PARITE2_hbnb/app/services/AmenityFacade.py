from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class AmenityFacade():
    def __init__(self):
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            return None  # Return None if the name is empty
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Vérifie que cette ligne ne retourne pas `None`
        amenities = self.db_session.query(Amenity).all()
        return amenities if amenities else []

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            self.amenity_repo.update(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        amenities = self.amenity_repo.get_all()
        for amenity in amenities:
            if amenity.name == name:
                return amenity
        return None

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)
