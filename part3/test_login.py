import unittest
import requests

BASE_URL = "http://localhost:5000"

class TestJWTAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur de test et stocker les tokens."""
        cls.test_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "securepassword123"
        }

        requests.post(f"{BASE_URL}/users/", json=cls.test_user)

    def test_1_login_success(self):
        """Test de connexion avec des identifiants valides."""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test.user@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

        self.__class__.access_token = response.json()["access_token"]

    def test_2_login_invalid_email(self):
        """Test de connexion avec un email inexistant."""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "invalid@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 401)

    def test_3_login_invalid_password(self):
        """Test de connexion avec un mot de passe incorrect."""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test.user@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)

    def test_4_access_protected_route_without_token(self):
        """Test d'accès à une route protégée sans token."""
        response = requests.get(f"{BASE_URL}/users/")
        self.assertEqual(response.status_code, 401)

    def test_5_access_protected_route_with_valid_token(self):
        """Test d'accès à une route protégée avec un token valide."""
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
