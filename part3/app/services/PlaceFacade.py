from app.models.place import Place
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade


amenityfacade = AmenityFacade()
userfacade = UsersFacade()

class PlaceFacade:

    def __init__(self):
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenityfacade = AmenityFacade()  # Correctement assigné comme attribut de classe
        self.userfacade = UsersFacade()  # Correctement assigné comme attribut de classe

    def create_place(self, place_data):
        """Crée un lieu."""
        existing_places = self.place_repo.get_all()
        for place in existing_places:
            if place.title == place_data.get("title"):
                print(f"Title '{place_data['title']}' already exists.")  # Debug
                return None  # Retourne None si le titre existe déjà
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner= self.userfacade.get_user(place_data["owner_id"])  # Récupère l'utilisateur par son ID
        )
        if not place:
            print("Failed to create place.")
        self.place_repo.add(place)  # Ajoute le lieu à la base de données
        return place  # Retourne l'objet Place créé


    def get_place(self, place_id):
        """Récupère un lieu par son ID."""
        place = self.place_repo.get(place_id)
        if place:
            owner = self.userfacade.get_user(place.owner_id)  # Assure-toi que l'owner est un objet unique et pas une liste
            amenities = [self.amenityfacade.get_amenity(amenity_id) for amenity_id in place.amenities]
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
