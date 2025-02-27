from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade


amenityfacade = AmenityFacade()
userfacade = UsersFacade()

class PlaceFacade():

    def __init__(self):
        self.place_repo = InMemoryRepository()
        amenityfacade = AmenityFacade()
        userfacade = UsersFacade()

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            owner = userfacade.get_user(place.owner_id)  # Utilisation de la facade pour récupérer l'utilisateur
            amenities = [amenityfacade.get_amenity(amenity_id) for amenity_id in place.amenities]
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                } if owner else None,  # Si l'owner n'existe pas, retourner None
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in amenities if amenity]  # Filtrer les None si l'amenity n'est pas trouvé
            }
        return None



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