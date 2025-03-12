import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/auth/"

class TestJWTAuthentication(unittest.TestCase):
    """Suite de tests pour l'authentification JWT."""

    @classmethod
    def setUpClass(cls):
        """Crée un utilisateur de test avant d'exécuter les tests."""
        cls.test_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "TestPassword123"
        }

        cls.login_credentials = {
            "email": "test.user@example.com",
            "password": "TestPassword123"
        }

        # Créer un utilisateur de test
        user_creation_response = requests.post("http://localhost:5000/api/v1/users/", json=cls.test_user)
        print("📌 Réponse création utilisateur:", user_creation_response.status_code, user_creation_response.text)  # ✅ Debug

        if user_creation_response.status_code == 201:
            cls.user_id = user_creation_response.json().get("id")
        else:
            cls.user_id = None


    def test_1_login(self):
        """Test de connexion et récupération d'un token JWT."""
        response = requests.post(BASE_URL + "login", json=self.login_credentials)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)

        self.__class__.access_token = data["access_token"]
        self.__class__.refresh_token = data["refresh_token"]

    def test_2_protected_route_without_token(self):
        """Test d'accès à une route protégée sans token."""
        response = requests.get("http://localhost:5000/api/v1/protected")
        self.assertEqual(response.status_code, 401)

    def test_3_protected_route_with_token(self):
        """Test d'accès à une route protégée avec un token valide."""
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        response = requests.get("http://localhost:5000/api/v1/protected", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_4_refresh_token(self):
        """Test de rafraîchissement du token JWT."""
        headers = {"Authorization": f"Bearer {self.__class__.refresh_token}"}
        response = requests.post(BASE_URL + "refresh", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)

    @classmethod
    def tearDownClass(cls):
        """Supprime l'utilisateur de test après les tests."""
        if cls.user_id:
            requests.delete(f"http://localhost:5000/api/v1/users/{cls.user_id}")

if __name__ == "__main__":
    unittest.main()
