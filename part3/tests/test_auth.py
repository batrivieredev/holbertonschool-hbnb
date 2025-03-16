import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/auth"

class TestAuthAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "securepassword123"
        }
        cls.login_data = {"email": cls.test_user["email"], "password": cls.test_user["password"]}

        # Vérifier si le serveur est en ligne
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 404:
                raise unittest.SkipTest("⚠️ Serveur non disponible ou endpoint incorrect.")
        except requests.exceptions.ConnectionError:
            raise unittest.SkipTest("⚠️ Impossible de se connecter au serveur.")

        # Création de l'utilisateur si inexistant
        requests.post(f"{BASE_URL}/register", json=cls.test_user)

    def test_1_login_success(self):
        """Test de connexion avec des identifiants valides"""
        response = requests.post(f"{BASE_URL}/login", json=self.login_data)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("access_token", response.json())

    def test_2_login_failure_invalid_password(self):
        """Test de connexion avec un mot de passe incorrect"""
        data = {"email": self.test_user["email"], "password": "wrongpassword"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        self.assertEqual(response.status_code, 401, response.text)

    def test_3_login_failure_invalid_email(self):
        """Test de connexion avec un email inexistant"""
        data = {"email": "nouser@example.com", "password": "password"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        self.assertEqual(response.status_code, 401, response.text)

if __name__ == "__main__":
    unittest.main()
