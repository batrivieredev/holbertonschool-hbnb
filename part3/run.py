"""
Point d'entrée pour le serveur de développement.
Lance l'application Flask en mode debug.

Usage:
    python run.py

Options:
    --port: Port d'écoute (défaut: 5000)
    --host: Host d'écoute (défaut: localhost)
"""

from app import create_app
from setup_db import reset_database, clean_database

# Créer l'application avec la configuration par défaut
app = create_app()

def init_app():
    """Initialiser l'application et la base de données"""
    # Réinitialiser et nettoyer la base de données
    reset_database()
    clean_database()
    return app

if __name__ == '__main__':
    # Obtenir l'instance de l'application initialisée
    flask_app = init_app()
    # Lancer le serveur en mode debug
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
