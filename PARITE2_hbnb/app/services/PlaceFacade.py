from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade
from datetime import datetime

amenityfacade = AmenityFacade()
userfacade = UsersFacade()

class PlaceFacade():

    def __init__(self):
        self.place_repo = InMemoryRepository()
        self.amenityfacade = AmenityFacade()
        self.userfacade = UsersFacade()

    def create_place(self, place_data):
        print(f"🔍 Debug: Checking for duplicates...")

        existing_places = self.place_repo.get_all()
        print(f"📦 Debug: Current stored places: {existing_places}")

        for place in existing_places:
            if isinstance(place, dict):
                continue

            if place.title == place_data["title"] and place.latitude == place_data["latitude"] and place.longitude == place_data["longitude"]:
                raise ValueError("A place with the same title and location already exists")

        owner_id = place_data.get("owner_id")
        owner = userfacade.get_user(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id: User not found")

        # 🔥 Vérifier que `amenities` est une liste valide
        amenities = place_data.get("amenities")
        if amenities is None or not isinstance(amenities, list):
            return {"error": "Amenities must be a list of amenity IDs"}, 400
        if len(amenities) == 0:
            return {"error": "At least one amenity is required"}, 400  # 🔥 Bloque si la liste est vide

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner,
            amenities=amenities  # 🔥 Stocke les amenities correctement
        )

        self.place_repo.add(place)
        return place



    def get_place(self, place_id):
        print(f"🔍 Debug: Searching for place ID {place_id}")
        place = self.place_repo.get(place_id)
        print(f"🔍 Debug: Found place: {place}")
        return place

    def update_place(self, place_id, place_data):
        print(f"🔍 Debug: Trying to update place with ID {place_id}")

        place = self.place_repo.get(place_id)
        print(f"🔍 Debug: Found place: {place}")

        if not place:
            print("❌ Debug: Place not found!")
            return None

        if not isinstance(place_data, dict):  # 🔥 Vérifier que place_data est bien un dict
            print(f"❌ Debug: place_data is not a dictionary: {place_data}")
            return None

        for key, value in place_data.items():
            if hasattr(place, key) and value is not None:
                setattr(place, key, value)

        place.updated_at = datetime.now()
        self.place_repo.update(place.id, vars(place))  # 🔥 Convertir en dict avant mise à jour

        print(f"✅ Debug: Place updated successfully: {place}")
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        print(f"🔍 Debug: Places found in repository: {places}")  # Debug

        if not places:
            return []

        formatted_places = []
        for place in places:
            if isinstance(place, dict):  # 🔥 Vérifier si c'est un dict au lieu d'un objet
                print("⚠️ Warning: Found a dictionary instead of a Place object!")
                continue  # Ignore les dicts corrompus

            formatted_places.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                } if place.owner else None,
                'amenities': place.amenities,
                'reviews': place.reviews
            })

        return formatted_places
