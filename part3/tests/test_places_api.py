import unittest
import requests

BASE_URL = "http://localhost:5000/places/"

class TestPlaceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_place = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100,
            'latitude': 37.773972,
            'longitude': -122.431297
        }
        response = requests.post(BASE_URL, json=cls.test_place)
        if response.status_code == 201:
            cls.place_id = response.json().get('id')

    def test_1_get_all_places(self):
        """Test de récupération de tous les lieux."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_2_get_place_by_id(self):
        """Test de récupération d'un lieu par ID."""
        response = requests.get(f"{BASE_URL}{self.place_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_update_place(self):
        """Test de mise à jour d'un lieu."""
        response = requests.put(f"{BASE_URL}{self.place_id}", json={"title": "Updated Title"})
        self.assertEqual(response.status_code, 200)

    def test_4_delete_place(self):
        """Test de suppression d'un lieu."""
        response = requests.delete(f"{BASE_URL}{self.place_id}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
