import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1"

class TestJWTAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Récupère le token admin pour les tests."""
        print("🔑 Tentative de connexion de l'admin...")

        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@hbnb.io",
            "password": "admin1234"  # ✅ On utilise l'admin déjà créé
        })
        print("🔑 Admin login response:", login_response.status_code, login_response.text)

        if login_response.status_code == 200:
            cls.admin_token = login_response.json()["access_token"]
        else:
            raise Exception("❌ Impossible de se connecter en tant qu'admin. Vérifiez la base de données et l'API.")

    def test_1_login_success(self):
        """Vérifie que l'admin peut se connecter."""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@hbnb.io",
            "password": "admin1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

        self.__class__.admin_token = response.json()["access_token"]

    def test_2_access_protected_route_without_token(self):
        """Vérifie qu'un accès sans token est refusé."""
        response = requests.get(f"{BASE_URL}/users/")
        self.assertEqual(response.status_code, 401)

    def test_3_access_protected_route_with_admin_token(self):
        """Vérifie qu'un admin peut accéder aux routes protégées."""
        headers = {"Authorization": f"Bearer {self.__class__.admin_token}"}
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        print("🔍 Admin access response:", response.status_code, response.text)
        self.assertEqual(response.status_code, 200)  # ✅ Un admin doit pouvoir voir cette page

if __name__ == "__main__":
    unittest.main()
