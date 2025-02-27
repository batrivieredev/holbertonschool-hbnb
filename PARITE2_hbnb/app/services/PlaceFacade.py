from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class PlaceFacade():
    def __init__(self):
        self.place_repo = InMemoryRepository()

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Récupérer tous les lieux."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            self.place_repo.update(place.id, place_data)
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)