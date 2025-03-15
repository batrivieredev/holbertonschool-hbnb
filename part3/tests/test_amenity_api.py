import unittest
import requests

BASE_URL = "http://localhost:5000/amenities/"

class TestAmenitiesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_amenity = {'name': 'Piscine'}

        response = requests.post(BASE_URL, json=cls.test_amenity)
        if response.status_code == 201:
            cls.amenity_id = response.json().get("id")
        else:
            cls.amenity_id = None

    def test_1_get_all_amenities(self):
        """Test de récupération de toutes les amenities."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_2_get_amenity_by_id(self):
        """Test de récupération d'une amenity par ID."""
        if not self.amenity_id:
            self.skipTest("L'amenity de test n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.amenity_id}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
