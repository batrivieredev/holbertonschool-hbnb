import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/users/"

class TestUsersAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur une seule fois pour tous les tests."""
        cls.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        cls.updated_user = {
            "first_name": "Johnny",
            "last_name": "D.",
            "email": "johnny.d@example.com"
        }

        response = requests.post(BASE_URL, json=cls.test_user)
        if response.status_code == 201:
            cls.user_id = response.json().get("id")
        else:
            cls.user_id = None

    def test_1_create_duplicate_user(self):
        """Test de création d'un utilisateur avec un email déjà existant."""
        response = requests.post(BASE_URL, json=self.test_user)
        self.assertEqual(response.status_code, 400)  # Doit renvoyer une erreur

    def test_2_get_user_by_id(self):
        """Test de récupération d'un utilisateur par ID."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_users(self):
        """Test de récupération de tous les utilisateurs."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_4_update_user(self):
        """Test de mise à jour d'un utilisateur."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.put(f"{BASE_URL}{self.user_id}", json=self.updated_user)
        self.assertEqual(response.status_code, 200)

    def test_5_get_updated_user(self):
        """Vérifie si la mise à jour a bien été effectuée."""
        if not self.user_id:
            self.skipTest("L'utilisateur n'a pas été créé")
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], self.updated_user["first_name"])

    def test_6_get_nonexistent_user(self):
        """Test de récupération d'un utilisateur inexistant."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)

    def test_7_update_nonexistent_user(self):
        """Test de mise à jour d'un utilisateur inexistant."""
        response = requests.put(f"{BASE_URL}nonexistent-id", json=self.updated_user)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
