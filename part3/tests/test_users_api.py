import unittest
import requests

BASE_URL = "http://localhost:5000/users/"
AUTH_URL = "http://localhost:5000/auth/login"

class TestUsersAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur de test."""
        cls.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword123"
        }
        response = requests.post(BASE_URL, json=cls.test_user)
        if response.status_code == 201:
            cls.user_id = response.json().get("id")

        login_data = {
            "email": cls.test_user["email"],
            "password": cls.test_user["password"]
        }
        login_response = requests.post(AUTH_URL, json=login_data)
        if login_response.status_code == 200:
            cls.access_token = login_response.json().get("access_token")

    def test_1_create_duplicate_user(self):
        """Test de création d'un utilisateur avec un email déjà existant."""
        response = requests.post(BASE_URL, json=self.test_user)
        self.assertEqual(response.status_code, 400)

    def test_2_get_user_by_id(self):
        """Test de récupération d'un utilisateur par ID."""
        response = requests.get(f"{BASE_URL}{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_3_get_all_users(self):
        """Test de récupération de tous les utilisateurs."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_4_update_user(self):
        """Test de mise à jour des informations de l'utilisateur."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.put(f"{BASE_URL}{self.user_id}", json={
            "first_name": "UpdatedName",
            "last_name": "UpdatedLast"
        }, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_5_delete_user(self):
        """Test de suppression d'un utilisateur."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.delete(f"{BASE_URL}{self.user_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
