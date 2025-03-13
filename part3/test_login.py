import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1"

class TestJWTAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un utilisateur pour les tests et stocker les tokens."""
        cls.test_user = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "securepassword123"
        }

        # Création de l'utilisateur
        print("📌 Tentative de création de l'utilisateur...")
        response = requests.post(f"{BASE_URL}/users/", json=cls.test_user)
        print(f"📌 Réponse création utilisateur: {response.status_code} {response.json()}")

        if response.status_code == 201:
            cls.user_id = response.json().get("id")
        else:
            cls.user_id = None

    def test_1_login(self):
        """Test de connexion et récupération d'un token JWT."""
        login_data = {
            "email": self.__class__.test_user["email"],
            "password": self.__class__.test_user["password"]
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)  # ✅ FIXED URL
        print(f"📌 Réponse login: {response.status_code} {response.json()}")

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("access_token", json_response)
        self.assertIn("refresh_token", json_response)  # ✅ Ensure refresh token is received

        self.__class__.access_token = json_response["access_token"]
        self.__class__.refresh_token = json_response["refresh_token"]

    def test_2_protected_route_without_token(self):
        """Test d'accès à une route protégée sans token."""
        response = requests.get(f"{BASE_URL}/protected/")  # ✅ FIXED URL
        print(f"📌 Réponse accès sans token: {response.status_code} {response.json()}")
        self.assertEqual(response.status_code, 401)

    def test_3_protected_route_with_token(self):
        """Test d'accès à une route protégée avec un token valide."""
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        response = requests.get(f"{BASE_URL}/protected/", headers=headers)  # ✅ FIXED URL
        print(f"📌 Réponse accès avec token: {response.status_code} {response.json()}")
        self.assertEqual(response.status_code, 200)

    def test_4_refresh_token(self):
        """Test de rafraîchissement du token JWT."""
        headers = {"Authorization": f"Bearer {self.__class__.refresh_token}"}
        response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)  # ✅ FIXED URL
        print(f"📌 Réponse refresh token: {response.status_code} {response.json()}")

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("access_token", json_response)

        # ✅ Update new access token for further tests
        self.__class__.access_token = json_response["access_token"]

if __name__ == "__main__":
    unittest.main()
