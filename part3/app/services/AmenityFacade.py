from app.models.amenity import Amenity
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository

class AmenityFacade():
    def __init__(self):
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_amenity(self, amenity_data):
        """Créer une nouvelle amenity."""
        name = amenity_data.get('name')
        if not name or not isinstance(name, str) or name.strip() == "":
            return None
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Récupérer une amenity par ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Récupérer toutes les amenities."""
        amenities = self.amenity_repo.get_all()
        return amenities if amenities else []

    def update_amenity(self, amenity_id, amenity_data):
        print(f"🔍 Debug: Tentative de mise à jour de l'amenity {amenity_id} avec {amenity_data}")

        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            print("❌ Amenity non trouvée !")
            return None  # Correction : évite une erreur 500

        # Vérifier que 'name' est bien fourni et valide
        name = amenity_data.get("name")
        if not name or not isinstance(name, str) or name.strip() == "":
            print("❌ Données invalides pour la mise à jour !")
            return None  # Correction : éviter une mise à jour invalide

        # Appliquer la mise à jour
        amenity.name = name
        self.amenity_repo.update(amenity.id, {'name': amenity.name})

        print(f"✅ Mise à jour réussie : {amenity}")
        return amenity


    def get_amenity_by_name(self, name):
        """Rechercher une amenity par son nom."""
        amenities = self.amenity_repo.get_all()
        for amenity in amenities:
            if amenity.name == name:
                return amenity
        return None

    def delete_amenity(self, amenity_id):
        """Supprimer une amenity."""
        return self.amenity_repo.delete(amenity_id)
