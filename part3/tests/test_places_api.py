import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/places"

class TestPlacesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_place = {
            "title": "Appartement cosy",
            "description": "Très bel appartement en centre-ville",
            "price": 100.00,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": "test_owner_id"
        }

        # Création du lieu
        response = requests.post(BASE_URL, json=cls.test_place)
        if response.status_code == 201:
            cls.place_id = response.json().get("id")
        else:
            cls.place_id = None

    def test_1_get_all_places(self):
        """Test récupération de tous les lieux"""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_2_get_place_details(self):
        """Test récupération des détails d'un lieu"""
        response = requests.get(f"{BASE_URL}/{self.place_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_update_place(self):
        """Test mise à jour d'un lieu"""
        updated_place = {"title": "Appartement luxueux"}
        response = requests.put(f"{BASE_URL}/{self.place_id}", json=updated_place)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
