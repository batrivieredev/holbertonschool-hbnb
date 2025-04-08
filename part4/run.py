"""
Point d'entrée pour le serveur de développement.
Lance l'application Flask en mode debug.

Usage:
    python run.py [--reset-db]

Options:
    --reset-db : Réinitialiser la base de données avant de démarrer
"""
#!/usr/bin/env python3
import argparse
import os
from flask import send_from_directory
from app import create_app
from setup_db import init_database, reset_database
from create_admin import create_admin

def main():
    parser = argparse.ArgumentParser(description="Lance l'application Flask.")
    parser.add_argument('--reset-db', action='store_true', help="Réinitialiser la base de données avant de démarrer")
    args = parser.parse_args()

    # Crée l'application avec la configuration par défaut
    app = create_app()

    if args.reset_db:
        print("🔄 Réinitialisation de la base de données...")
        with app.app_context():
            reset_database()
            print("✅ Base de données réinitialisée avec succès.")
            # Create admin user after database reset
            create_admin()
    else:
        with app.app_context():
            init_database()
            # Ensure admin exists even without reset
            create_admin()

    # Routes pour servir les fichiers statiques
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(app.root_path, '../static/css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(app.root_path, '../static/js'), filename)

    print("🚀 Serveur en cours d'exécution sur http://localhost:5001/")
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    main()
