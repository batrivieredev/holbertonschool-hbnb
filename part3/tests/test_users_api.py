import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1/users"
AUTH_URL = "http://localhost:5000/api/v1/auth/login"

class TestUsersAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer un administrateur et récupérer un token JWT admin."""
        cls.admin_login = {
            "email": "admin@hbnb.io",
            "password": "admin1234"
        }

        cls.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe{uuid.uuid4()}@example.com",  # Email unique
            "password": "securepassword123"
        }
        cls.updated_user = {"first_name": "Johnny", "last_name": "D."}

        # Connexion en tant qu'admin
        admin_response = requests.post(AUTH_URL, json=cls.admin_login)
        if admin_response.status_code == 200:
            json_data = admin_response.json()
            cls.admin_token = json_data.get("access_token")
            cls.admin_id = json_data.get("user", {}).get("id")
            print(f"✅ Token admin récupéré : {cls.admin_token}")
        else:
            cls.admin_token = None
            cls.admin_id = None
            print(f"❌ Échec connexion admin : {admin_response.status_code} {admin_response.text}")
            raise unittest.SkipTest("Impossible de récupérer un token admin.")

        # Création d'un utilisateur test (via admin)
        headers = {"Authorization": f"Bearer {cls.admin_token}"}
        response = requests.post(BASE_URL, json=cls.test_user, headers=headers)
        if response.status_code == 201:
            cls.user_id = response.json().get("id")
            print(f"✅ Utilisateur test créé avec ID : {cls.user_id}")
        else:
            cls.user_id = None
            print(f"❌ Erreur création utilisateur test : {response.status_code} {response.text}")
            raise unittest.SkipTest("Impossible de créer l'utilisateur test.")

    def test_1_get_all_users(self):
        """Test récupération de tous les utilisateurs (admin only)."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(BASE_URL, headers=headers)
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_2_admin_update_user(self):
        """Test mise à jour d'un utilisateur par un admin."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/{self.user_id}", json=self.updated_user, headers=headers)

        print(f"📌 Réponse update user (admin): {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["first_name"], self.updated_user["first_name"])

    def test_3_get_user_by_id(self):
        """Test récupération d'un utilisateur par ID."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(f"{BASE_URL}/{self.user_id}", headers=headers)

        print(f"📌 Réponse get user by ID: {response.status_code} {response.text}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["id"], self.user_id)

    def test_4_get_nonexistent_user(self):
        """Test récupération d'un utilisateur inexistant."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(f"{BASE_URL}/nonexistent-id", headers=headers)
        self.assertEqual(response.status_code, 404, response.text)

    def test_5_update_nonexistent_user(self):
        """Test mise à jour d'un utilisateur inexistant (admin)."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/nonexistent-id", json=self.updated_user, headers=headers)

        print(f"📌 Réponse update non-existent user (admin): {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 404, response.text)

    def test_6_password_not_returned_in_response(self):
        """Test pour s'assurer que le mot de passe n'est pas retourné après la création."""
        new_user = {
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": f"alice{uuid.uuid4()}@example.com",  # Email unique
            "password": "mypassword"
        }
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.post(BASE_URL, json=new_user, headers=headers)

        print(f"📌 Réponse création user Alice: {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 201, response.text)
        self.assertNotIn("password", response.json(), response.text)

    def test_7_invalid_email_format(self):
        """Test de création d'un utilisateur avec un email invalide."""
        invalid_user = self.test_user.copy()
        invalid_user["email"] = "invalid-email"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.post(BASE_URL, json=invalid_user, headers=headers)

        print(f"📌 Réponse création user avec email invalide: {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 400, response.text)

    def test_8_update_user_with_email(self):
        """Test de mise à jour de l'email (ce qui doit être autorisé pour un admin)."""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/{self.user_id}", json={"email": "new.email@example.com"}, headers=headers)

        print(f"📌 Réponse update email (admin): {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 200, response.text)

    def test_9_non_admin_cannot_update_user(self):
        """Test qu'un utilisateur normal ne peut pas modifier un autre utilisateur."""
        user_login = {"email": self.test_user["email"], "password": self.test_user["password"]}
        user_response = requests.post(AUTH_URL, json=user_login)

        if user_response.status_code == 200:
            user_token = user_response.json().get("access_token")
        else:
            self.skipTest("⚠️ Impossible de récupérer le token utilisateur.")

        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.put(f"{BASE_URL}/{self.admin_id}", json={"first_name": "Hack"}, headers=headers)

        print(f"📌 Réponse update admin as normal user: {response.status_code} {response.text}")

        self.assertEqual(response.status_code, 403, response.text)

if __name__ == "__main__":
    unittest.main()
