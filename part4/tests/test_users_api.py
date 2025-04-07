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
            "email": "admin2@hbnb.io",
            "password": "admin12345"
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
            print(f"❌ Erreur création utilisateur test : {response.status_code} {response.text}")
            raise unittest.SkipTest("Impossible de créer l'utilisateur test.")

        # 🔍 Debug: Vérification de la création de l'utilisateur
        user_check = requests.get(f"{BASE_URL}/{cls.user_id}", headers=headers)
        print(f"📌 Vérification utilisateur test: {user_check.status_code} {user_check.text}")

        # ✅ Tentative de connexion de l'utilisateur normal pour obtenir un token
        user_login_response = requests.post(AUTH_URL, json={"email": cls.test_user["email"], "password": cls.test_user["password"]})
        
        if user_login_response.status_code == 200:
            cls.user_token = user_login_response.json().get("access_token")
            print(f"✅ Token utilisateur récupéré : {cls.user_token}")
        else:
            cls.user_token = None
            print(f"❌ Échec connexion utilisateur test : {user_login_response.status_code} {user_login_response.text}")


    def test_1_get_all_users(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(BASE_URL, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_2_admin_update_user(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/{self.user_id}", json=self.updated_user, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_3_get_user_by_id(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(f"{BASE_URL}/{self.user_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_4_get_nonexistent_user(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(f"{BASE_URL}/nonexistent-id", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_5_update_nonexistent_user(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/nonexistent-id", json=self.updated_user, headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_6_password_not_returned_in_response(self):
        new_user = {
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": f"alice{uuid.uuid4()}@example.com",
            "password": "mypassword"
        }
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.post(BASE_URL, json=new_user, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())

    def test_7_invalid_email_format(self):
        invalid_user = self.test_user.copy()
        invalid_user["email"] = "invalid-email"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.post(BASE_URL, json=invalid_user, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_8_update_user_with_email(self):
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        new_email = f"new.email{uuid.uuid4()}@example.com"
        response = requests.put(f"{BASE_URL}/{self.user_id}", json={"email": new_email}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], new_email)

    def test_9_non_admin_cannot_update_user(self):
        user_login = {"email": self.test_user["email"], "password": self.test_user["password"]}
        user_response = requests.post(AUTH_URL, json=user_login)
        if user_response.status_code == 200:
            user_token = user_response.json().get("access_token")
        else:
            self.skipTest("Impossible de récupérer le token utilisateur.")
        
        headers = {"Authorization": f"Bearer {user_token}"}
        response = requests.put(f"{BASE_URL}/{self.admin_id}", json={"first_name": "Hack"}, headers=headers)
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
