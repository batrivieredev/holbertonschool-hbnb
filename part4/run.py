#!/usr/bin/env python3
"""Point d'entrée principal de l'application HBNB"""
import os
import sys
from app import create_app
from setup_db import init_db
from create_admin import create_admin

def main():
    """Initialise et démarre l'application"""
    try:
        # Création de l'instance Flask
        app = create_app()

        # Initialisation de la base de données si nécessaire
        if not init_db(app):
            print("❌ Échec de l'initialisation de la base de données")
            sys.exit(1)

        # Création de l'utilisateur admin si nécessaire
        if not create_admin():
            print("❌ Échec de la création de l'administrateur")
            sys.exit(1)

        # Configuration du serveur
        host = os.getenv('FLASK_HOST', '0.0.0.0')  # Interface d'écoute
        port = int(os.getenv('FLASK_PORT', 5001))  # Port d'écoute
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'  # Mode debug

        # Démarrage du serveur
        print(f"🚀 Serveur en cours d'exécution sur http://localhost:{port}/")
        app.run(host=host, port=port, debug=debug)

    except Exception as e:
        print(f"❌ Erreur de démarrage de l'application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
