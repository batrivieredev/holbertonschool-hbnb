from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade
from datetime import datetime

amenityfacade = AmenityFacade()
userfacade = UsersFacade()

class PlaceFacade:

    def __init__(self):
        self.place_repo = InMemoryRepository()
<<<<<<< HEAD
        self.amenityfacade = AmenityFacade()  # Correctement assigné comme attribut de classe
        self.userfacade = UsersFacade()  # Correctement assigné comme attribut de classe

    def create_place(self, place_data):
        """Crée un lieu."""
        existing_places = self.place_repo.get_all()
        for place in existing_places:
            if place.title == place_data.get("title"):
                print(f"Title '{place_data['title']}' already exists.")  # Debug
                return None  # Retourne None si le titre existe déjà
=======
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

>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
<<<<<<< HEAD
            owner= self.userfacade.get_user(place_data["owner_id"])  # Récupère l'utilisateur par son ID
        )
        if not place:
            print("Failed to create place.")
        self.place_repo.add(place)  # Ajoute le lieu à la base de données
        return place  # Retourne l'objet Place créé

=======
            owner=owner,
            amenities=amenities  # 🔥 Stocke les amenities correctement
        )

        self.place_repo.add(place)
        return place
>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb



    def get_place(self, place_id):
<<<<<<< HEAD
        """Récupère un lieu par son ID."""
        place = self.place_repo.get(place_id)
        if place:
            owner = self.userfacade.get_user(place.owner_id)  # Assure-toi que l'owner est un objet unique et pas une liste
            amenities = [self.amenityfacade.get_amenity(amenity_id) for amenity_id in place.amenities]
            return {
=======
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
>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
<<<<<<< HEAD
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                } if owner else None,  # Vérifie si l'owner existe
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in amenities if amenity],  # Filtre les None
            }
        return None

    def get_all_places(self):
        """Récupérer tous les lieux sans erreur même si aucun n'existe."""
        places = self.place_repo.get_all()
        if places is None:
            return []
        return places

    def update_place(self, place_id, place_data):
        """Met à jour un lieu."""
        place = self.place_repo.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            self.place_repo.update(place.id, place_data)
        return place

    def delete_place(self, place_id):
        """Supprimer un lieu."""
        return self.place_repo.delete(place_id)
=======
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                } if place.owner else None,
                'amenities': place.amenities,
                'reviews': place.reviews
            })

        return formatted_places
>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb
