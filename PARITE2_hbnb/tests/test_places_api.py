import unittest
from unittest.mock import MagicMock
from app.models.place import Place
from app.services.PlaceFacade import PlaceFacade
from app.services.AmenityFacade import AmenityFacade
from app.services.UsersFacade import UsersFacade

class TestPlaceFacade(unittest.TestCase):

    def setUp(self):
        # Mocks des facades
        self.amenityfacade = MagicMock(spec=AmenityFacade)
        self.userfacade = MagicMock(spec=UsersFacade)

        # Création de l'instance de la PlaceFacade avec les facades simulées
        self.place_facade = PlaceFacade()
        self.place_facade.amenityfacade = self.amenityfacade
        self.place_facade.userfacade = self.userfacade

        # Mocks des repositorys
        self.place_repo = MagicMock()
        self.place_facade.place_repo = self.place_repo

    def test_create_place(self):
        """Test pour la création d'un lieu"""
        place_data = {
            'title': "Test Place",
            'description': "A nice place",
            'price': 100,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': 1,
            'amenities': [1, 2]
        }

        # Simule l'ajout d'une place
        place = Place(**place_data)
        self.place_repo.add.return_value = place

        result = self.place_facade.create_place(place_data)

        self.assertEqual(result.title, "Test Place")
        self.assertEqual(result.description, "A nice place")
        self.assertEqual(result.price, 100)
        self.assertEqual(result.latitude, 48.8566)
        self.assertEqual(result.longitude, 2.3522)
        self.assertEqual(result.owner_id, 1)
        self.assertEqual(result.amenities, [1, 2])
        self.place_repo.add.assert_called_with(place)

    def test_get_place_success(self):
        """Test pour récupérer un lieu valide"""
        place = MagicMock()
        place.id = 1
        place.title = "Test Place"
        place.description = "A nice place"
        place.price = 100
        place.latitude = 48.8566
        place.longitude = 2.3522
        place.owner_id = 2
        place.amenities = [1, 2]

        # Mocks des facades
        owner = MagicMock(id=2, first_name="John", last_name="Doe", email="john.doe@example.com")
        amenity1 = MagicMock(id=1, name="Pool")
        amenity2 = MagicMock(id=2, name="Gym")
        
        self.place_repo.get.return_value = place
        self.userfacade.get_user.return_value = owner
        self.amenityfacade.get_amenity.side_effect = [amenity1, amenity2]

        result = self.place_facade.get_place(1)

        self.assertEqual(result['id'], 1)
        self.assertEqual(result['title'], "Test Place")
        self.assertEqual(result['owner']['id'], 2)
        self.assertEqual(result['amenities'][0]['name'], "Pool")
        self.assertEqual(result['amenities'][1]['name'], "Gym")

    def test_get_place_not_found(self):
        """Test pour vérifier si un lieu inexistant retourne None"""
        self.place_repo.get.return_value = None

        result = self.place_facade.get_place(999)  # ID qui n'existe pas

        self.assertIsNone(result)

    def test_update_place(self):
        """Test pour mettre à jour un lieu"""
        place = MagicMock()
        place.id = 1
        place.title = "Old Place"
        place.description = "Old description"
        place.price = 50
        place.latitude = 48.8566
        place.longitude = 2.3522

        updated_data = {
            'title': "Updated Place",
            'description': "Updated description",
            'price': 120
        }

        self.place_repo.get.return_value = place
        self.place_repo.update.return_value = place

        result = self.place_facade.update_place(1, updated_data)

        self.assertEqual(result.title, "Updated Place")
        self.assertEqual(result.description, "Updated description")
        self.assertEqual(result.price, 120)
        self.place_repo.update.assert_called_with(1, updated_data)

    def test_delete_place(self):
        """Test pour supprimer un lieu"""
        place = MagicMock()
        place.id = 1

        self.place_repo.get.return_value = place
        self.place_repo.delete.return_value = True

        result = self.place_facade.delete_place(1)

        self.assertTrue(result)
        self.place_repo.delete.assert_called_with(1)

    def test_get_all_places(self):
        """Test pour récupérer toutes les places"""
        place1 = MagicMock(id=1, title="Place 1")
        place2 = MagicMock(id=2, title="Place 2")

        self.place_repo.get_all.return_value = [place1, place2]

        result = self.place_facade.get_all_places()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], "Place 1")
        self.assertEqual(result[1]['title'], "Place 2")

    def test_create_place_invalid_data(self):
        """Test pour créer un lieu avec des données invalides"""
        place_data = {
            'title': "",
            'description': "A nice place",
            'price': 100,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': 1,
            'amenities': [1, 2]
        }

        result = self.place_facade.create_place(place_data)

        self.assertIsNone(result)  # Le titre est requis, donc la création échoue

    def test_get_place_with_missing_amenity(self):
        """Test pour récupérer un lieu avec une amenity manquante"""
        place = MagicMock()
        place.id = 1
        place.owner_id = 2
        place.amenities = [1, 99]  # L'ID 99 n'existe pas dans les amenities

        owner = MagicMock(id=2, first_name="John", last_name="Doe", email="john.doe@example.com")
        amenity1 = MagicMock(id=1, name="Pool")
        
        self.place_repo.get.return_value = place
        self.userfacade.get_user.return_value = owner
        self.amenityfacade.get_amenity.side_effect = [amenity1, None]  # Amenity 99 est manquante

        result = self.place_facade.get_place(1)

        self.assertEqual(len(result['amenities']), 1)  # L'amenity manquante ne doit pas être incluse
        self.assertEqual(result['amenities'][0]['name'], "Pool")

    def test_update_place_invalid_data(self):
        """Test pour une tentative de mise à jour avec des données invalides"""
        place = MagicMock()
        place.id = 1
        place.title = "Test Place"
        place.description = "Old description"
        place.price = 50
        place.latitude = 48.8566
        place.longitude = 2.3522

        self.place_repo.get.return_value = place
        updated_data = {
            'title': "",  # Titre invalide
            'description': "Updated description",
            'price': 120
        }

        result = self.place_facade.update_place(1, updated_data)

        self.assertIsNone(result)  # Mise à jour échouée car le titre est vide

    def test_delete_place_not_found(self):
        """Test pour supprimer un lieu qui n'existe pas"""
        self.place_repo.get.return_value = None

        result = self.place_facade.delete_place(999)

        self.assertFalse(result)  # La place n'existe pas, donc la suppression échoue

    def test_create_place_with_non_existent_user(self):
        """Test pour créer une place avec un owner_id inexistant"""
        place_data = {
            'title': "Test Place",
            'description': "A nice place",
            'price': 100,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': 999,  # Owner inexistant
            'amenities': [1, 2]
        }

        # Simule que l'utilisateur avec ID 999 n'existe pas
        self.userfacade.get_user.return_value = None

        result = self.place_facade.create_place(place_data)

        self.assertIsNone(result)  # L'owner n'existe pas, donc la création échoue

    def test_get_all_places_empty(self):
        """Test pour récupérer toutes les places quand il n'y en a pas"""
        self.place_repo.get_all.return_value = []

        result = self.place_facade.get_all_places()

        self.assertEqual(len(result), 0)  # Pas de places dans la base de données

if __name__ == '__main__':
    unittest.main()
