import unittest
import requests
import time
import concurrent.futures
from dotenv import load_dotenv
import os
import psutil

load_dotenv()

BASE_URL = "http://localhost:5000/api/v1"
API_TOKEN = os.getenv('API_TOKEN', 'default_token')

class TestPerformance(unittest.TestCase):
    """Tests de performance pour l'API"""

    @classmethod
    def setUpClass(cls):
        """Vérifie que le serveur est accessible"""
        cls.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        # Vérifier si le serveur est en marche
        try:
            requests.get(f"{BASE_URL}/", timeout=1)
        except requests.exceptions.ConnectionError:
            raise unittest.SkipTest(
                "Le serveur n'est pas accessible. Lancez d'abord 'python run.py'"
            )

    def test_response_time(self):
        """Vérifier les temps de réponse"""
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/places/", headers=self.headers)
            print(f"réponse: {response}s")
            duration = time.time() - start
            self.assertLess(duration, 1.0)  # Max 1s en dev
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            self.skipTest("Le serveur n'est pas accessible")

    def test_concurrent_requests(self):
        """Test de charge avec requêtes simultanées"""
        num_requests = 5  # Réduit pour les tests

        def make_request():
            try:
                return requests.get(f"{BASE_URL}/places/", headers=self.headers)
            except requests.exceptions.ConnectionError:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            responses = list(executor.map(lambda _: make_request(), range(num_requests)))

        # Vérifier les réponses valides
        valid_responses = [r for r in responses if r is not None]
        if not valid_responses:
            self.skipTest("Aucune réponse valide du serveur")

        for response in valid_responses:
            self.assertEqual(response.status_code, 200)

    def test_memory_usage(self):
        """Test de l'utilisation mémoire"""
        try:
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss

            # Faire 10 requêtes (réduit pour les tests)
            for _ in range(10):
                try:
                    requests.get(f"{BASE_URL}/places/", headers=self.headers)
                except requests.exceptions.ConnectionError:
                    self.skipTest("Le serveur n'est pas accessible")

            mem_after = process.memory_info().rss
            mem_increase = mem_after - mem_before

            # Vérifier que l'augmentation de mémoire est raisonnable (< 10MB)
            self.assertLess(mem_increase, 10 * 1024 * 1024)
        except ImportError:
            self.skipTest("psutil n'est pas installé")

if __name__ == '__main__':
    unittest.main()
