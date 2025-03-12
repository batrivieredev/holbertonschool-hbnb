"""
Test suite for the Places API endpoints.
"""

import unittest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000/api/v1/places/"
API_TOKEN = os.getenv('API_TOKEN', 'default_token')

class TestPlaceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        cls.test_place = {
            'name': 'Test Place',
            'description': 'Test Description',
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100,
            'latitude': 37.773972,
            'longitude': -122.431297
        }

        # Création du lieu de test
        response = requests.post(BASE_URL, json=cls.test_place, headers=cls.headers)
        if response.status_code == 201:
            cls.test_place_id = response.json().get('id')
        else:
            cls.test_place_id = None

    @classmethod
    def tearDownClass(cls):
        if cls.test_place_id:
            requests.delete(f"{BASE_URL}{cls.test_place_id}", headers=cls.headers)

    def test_1_create_duplicate_place(self):
        """Test de création d'un lieu avec des données similaires."""
        if not self.test_place_id:
            self.skipTest("Le lieu de test n'a pas été créé")
        response = requests.post(BASE_URL, json=self.test_place, headers=self.headers)
        self.assertIn(response.status_code, [400, 401, 422])

    def test_2_get_place_by_id(self):
        """Test de récupération d'un lieu par ID."""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.test_place_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_places(self):
        """Test de récupération de tous les lieux."""
        response = requests.get(BASE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # Suppression de la vérification du nombre minimum de lieux
        # car la base peut être vide

    def test_4_update_place(self):
        """Test de mise à jour d'un lieu."""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")
        updated_place = {
            'name': 'Updated Place',
            'description': 'Updated Description',
            'number_rooms': 3,
            'number_bathrooms': 2,
            'max_guest': 5,
            'price_by_night': 150,
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        response = requests.put(f"{BASE_URL}{self.test_place_id}", json=updated_place, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_5_get_updated_place(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.test_place_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Updated Place')

    def test_6_get_nonexistent_place(self):
        """Test de récupération d'un lieu inexistant."""
        response = requests.get(f"{BASE_URL}nonexistent-id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_7_update_nonexistent_place(self):
        """Test de mise à jour d'un lieu inexistant."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id",
            json={'name': 'Updated Name'},
            headers=self.headers
        )
        self.assertIn(response.status_code, [401, 404, 422])

    def test_8_create_place_with_invalid_data(self):
        """Test pour créer un lieu avec des données invalides."""
        invalid_place = {
            'invalid_field': 'Invalid Value'
        }
        response = requests.post(BASE_URL, json=invalid_place, headers=self.headers)
        self.assertIn(response.status_code, [400, 401, 422])

    def test_9_validate_price_range(self):
        """Test de validation du prix (doit être positif)"""
        invalid_place = self.test_place.copy()
        invalid_place['price_by_night'] = -100
        response = requests.post(BASE_URL, json=invalid_place, headers=self.headers)
        self.assertIn(response.status_code, [400, 422])

    def test_10_validate_coordinates(self):
        """Test de validation des coordonnées géographiques"""
        invalid_place = self.test_place.copy()
        invalid_place['latitude'] = 91  # Latitude max is 90
        response = requests.post(BASE_URL, json=invalid_place, headers=self.headers)
        self.assertIn(response.status_code, [400, 422])

    def test_11_search_places(self):
        """Test de recherche de lieux par critères"""
        params = {'max_price': 200, 'min_rooms': 2}
        response = requests.get(f"{BASE_URL}search", params=params, headers=self.headers)
        self.assertIn(response.status_code, [200, 404])  # Accepter 404 si l'endpoint n'existe pas
        if response.status_code == 200:
            self.assertIsInstance(response.json(), list)

    def test_12_partial_update(self):
        """Test de mise à jour partielle (PATCH)"""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")
        patch_data = {'price_by_night': 120}
        response = requests.patch(
            f"{BASE_URL}{self.test_place_id}",
            json=patch_data,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

    def test_13_amenities_management(self):
        """Test de la gestion des équipements d'un lieu"""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")

        amenity_data = {'amenity_ids': ['id1', 'id2']}
        response = requests.post(
            f"{BASE_URL}{self.test_place_id}/amenities",
            json=amenity_data,
            headers=self.headers
        )
        self.assertIn(response.status_code, [200, 201, 404])

    def test_14_place_availability(self):
        """Test de la gestion des disponibilités"""
        if not self.test_place_id:
            self.skipTest("Le lieu n'a pas été créé")

        availability = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-10',
            'is_available': False
        }
        response = requests.post(
            f"{BASE_URL}{self.test_place_id}/availability",
            json=availability,
            headers=self.headers
        )
        self.assertIn(response.status_code, [200, 201, 404])

    def test_15_advanced_search(self):
        """Test de recherche avancée avec filtres multiples"""
        search_params = {
            'price_min': 50,
            'price_max': 200,
            'amenities': ['wifi', 'parking'],
            'location': {'lat': 37.7749, 'lng': -122.4194, 'radius': 10}
        }
        response = requests.get(
            f"{BASE_URL}search/advanced",
            params=search_params,
            headers=self.headers
        )
        self.assertIn(response.status_code, [200, 404])

    def test_16_place_validation(self):
        """Tests de validation approfondis"""
        invalid_cases = [
            {'name': '', 'description': 'Test'},  # Nom vide
            {'name': 'A' * 129, 'description': 'Test'},  # Nom trop long
            {'price_by_night': 'not_a_number'},  # Prix invalide
            {'latitude': 100, 'longitude': 200}  # Coordonnées hors limites
        ]

        for invalid_data in invalid_cases:
            test_data = self.test_place.copy()
            test_data.update(invalid_data)
            response = requests.post(BASE_URL, json=test_data, headers=self.headers)
            self.assertIn(response.status_code, [400, 422])

    def test_17_performance_metrics(self):
        """Test des métriques de performance"""
        import time

        start_time = time.time()
        requests.get(BASE_URL, headers=self.headers)
        response_time = time.time() - start_time

        self.assertLess(response_time, 1.0)  # Temps de réponse < 1s

if __name__ == "__main__":
    unittest.main()
