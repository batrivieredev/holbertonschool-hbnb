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


reset_database()

clean_database()

app = create_app()

if __name__ == '__main__':
    # Active le mode debug pour le développement
    app.run(debug=True)
