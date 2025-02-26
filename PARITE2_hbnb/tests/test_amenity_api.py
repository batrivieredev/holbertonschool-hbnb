import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/amenities/"


class TestAmenitiesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer une amenity une seule fois pour tous les tests."""
        cls.test_amenity = {"name": "Pool"}
        cls.updated_amenity = {"name": "Luxury Pool"}

        response = requests.post(BASE_URL, json=cls.test_amenity)
        if response.status_code == 201:
            cls.amenity_id = response.json().get("id")
        else:
            cls.amenity_id = None

    def test_create_duplicate_amenity(self):
        """Test de création d'une amenity avec un nom déjà existant."""
        response = requests.post(BASE_URL, json=self.test_amenity)
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_by_id(self):
        """Test de récupération d'une amenity par ID."""
        if not self.amenity_id:
            self.skipTest("L'amenity n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.amenity_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_all_amenities(self):
        """Test de récupération de toutes les amenities."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_update_amenity(self):
        """Test de mise à jour d'une amenity."""
        if not self.amenity_id:
            self.skipTest("L'amenity n'a pas été créée")
        response = requests.put(
            f"{BASE_URL}{self.amenity_id}", json=self.updated_amenity)
        self.assertEqual(response.status_code, 200)

    def test_get_updated_amenity(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.amenity_id:
            self.skipTest("L'amenity n'a pas été créée")
        response = requests.get(f"{BASE_URL}{self.amenity_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.updated_amenity["name"])

    def test_get_nonexistent_amenity(self):
        """Test de récupération d'une amenity inexistante."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_amenity(self):
        """Test de mise à jour d'une amenity inexistante."""
        response = requests.put(
            f"{BASE_URL}nonexistent-id", json=self.updated_amenity)
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        """Test de suppression d'une amenity existante."""
        if not self.amenity_id:
            self.skipTest("L'amenity n'a pas été créée")
        response = requests.delete(f"{BASE_URL}{self.amenity_id}")
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_amenity(self):
        """Test de suppression d'une amenity inexistante."""
        response = requests.delete(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
