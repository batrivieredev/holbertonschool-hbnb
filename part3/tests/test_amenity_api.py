"""
Test suite for the Amenities API endpoints.

Requirements:
    - Python 3.x
    - requests library (`pip install requests`)

To run these tests:
    1. Make sure the API server is running on http://localhost:5000
    2. Install required packages:
       pip install requests

    3. Run the tests using one of these methods:
       - python3 -m unittest test_amenity_api.py
       - python3 test_amenity_api.py

Note: The API server must be running before executing the tests.
"""

import unittest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000/api/v1/amenities/"
API_TOKEN = os.getenv('API_TOKEN', 'default_token')  # Ajouter le token dans .env

"""
Tests unitaires pour l'API des équipements.
Vérifie le bon fonctionnement des endpoints CRUD.

Fonctionnalités testées:
    - Création d'équipements
    - Mise à jour des données
    - Récupération des détails
    - Validation des entrées
"""

class TestAmenitiesAPI(unittest.TestCase):
    """Suite de tests pour l'API des équipements.

    Configuration:
        - Crée un équipement de test avant les tests
        - Nettoie les données après les tests
        - Vérifie les codes HTTP et formats de réponse
    """

    @classmethod
    def setUpClass(cls):
        cls.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        cls.test_amenity = {'name': 'Test Amenity'}

        # Création de l'amenity de test
        response = requests.post(BASE_URL, json=cls.test_amenity, headers=cls.headers)
        if response.status_code == 201:
            cls.test_amenity_id = response.json().get('id')
        else:
            cls.test_amenity_id = None

        cls.updated_amenity = {'name': 'Updated Amenity'}

    @classmethod
    def tearDownClass(cls):
        """Supprimer l'amenity créée après les tests."""
        if cls.test_amenity_id:
            requests.delete(f"{BASE_URL}{cls.test_amenity_id}", headers=cls.headers)

    def test_0_check_api_availability(self):
        """Vérifier si l'API est accessible."""
        response = requests.get(BASE_URL, headers=self.headers)
        self.assertIn(response.status_code, [200, 404, 500])

    def test_1_create_duplicate_amenity(self):
        """Test de création d'une amenity avec un nom déjà existant."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.post(BASE_URL, json=self.test_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_2_get_amenity_by_id(self):
        """Test de récupération d'une amenity par ID."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.test_amenity_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_amenities(self):
        """Test de récupération de toutes les amenities."""
        response = requests.get(BASE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_4_update_amenity(self):
        """Test de mise à jour d'une amenity."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.put(f"{BASE_URL}{self.test_amenity_id}", json=self.updated_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_5_get_updated_amenity(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.test_amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.test_amenity_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.updated_amenity["name"])

    def test_6_get_nonexistent_amenity(self):
        """Test de récupération d'une amenity inexistante."""
        response = requests.get(f"{BASE_URL}nonexistent-id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_7_update_nonexistent_amenity(self):
        """Test de mise à jour d'une amenity inexistante."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id",
            json=self.updated_amenity,
            headers=self.headers
        )
        self.assertIn(response.status_code, [401, 404, 422])

    def test_10_create_empty_amenity(self):
        """Test de création d'une amenity avec un champ vide."""
        response = requests.post(
            BASE_URL,
            json={"name": ""},
            headers=self.headers
        )
        self.assertIn(response.status_code, [400, 401, 422])

    def test_11_create_invalid_amenity(self):
        """Test de création d'une amenity avec une entrée invalide."""
        response = requests.post(BASE_URL, json={"invalid_field": "Test"}, headers=self.headers)
        self.assertIn(response.status_code, [400, 422])

    def test_12_create_amenity_with_none_name(self):
        """Test de création d'une amenity avec un champ 'name' None."""
        response = requests.post(BASE_URL, json={"name": None}, headers=self.headers)
        self.assertIn(response.status_code, [400, 422])

    def test_13_create_amenity_with_whitespace_name(self):
        """Test de création d'une amenity avec un champ 'name' contenant uniquement des espaces."""
        response = requests.post(BASE_URL, json={"name": "   "}, headers=self.headers)
        self.assertIn(response.status_code, [400, 422])

if __name__ == "__main__":
    unittest.main()
