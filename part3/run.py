"""
Point d'entrée pour le serveur de développement.
Lance l'application Flask en mode debug.

Usage:
    python run.py [--reset-db]

Options:
    --reset-db : Réinitialiser la base de données avant de démarrer
"""

import sys
from app import create_app
from setup_db import reset_database

# Vérifie si --reset-db est passé en argument
reset_database()

# Créer l'application avec la configuration par défaut
app = create_app()

if __name__ == '__main__':
    print("🚀 Serveur en cours d'exécution sur http://localhost:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)
