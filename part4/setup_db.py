#!/usr/bin/env python3
"""Script d'initialisation de la base de données"""
import os
from app import create_app
from app.extensions import db, init_db_events
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def init_db(app):
    """Initialise la base de données et crée les tables si nécessaire"""
    print("🔄 Vérification de la base de données...")

    # Création du dossier d'instance si nécessaire
    if not os.path.exists(app.instance_path):
        print(f"📁 Création du dossier {app.instance_path}")
        os.makedirs(app.instance_path)

    db_path = os.path.join(app.root_path, 'hbnb.db')
    if not os.path.exists(db_path):
        print("📁 Création de la nouvelle base de données...")

        # Active le support des clés étrangères pour SQLite
        init_db_events()

        # Création des tables
        with app.app_context():
            db.create_all()
            print("✅ Tables créées avec succès.")

        # Création des équipements par défaut
        with app.app_context():
            default_amenities = [
                "WiFi", "Climatisation", "Chauffage", "Cuisine",
                "TV", "Parking gratuit", "Lave-linge", "Piscine",
                "Jacuzzi", "Salle de sport"
            ]

            for name in default_amenities:
                if not Amenity.query.filter_by(name=name).first():
                    amenity = Amenity(name=name)
                    db.session.add(amenity)

            try:
                db.session.commit()
                print("✅ Équipements par défaut créés.")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erreur lors de la création des équipements: {str(e)}")
                return False

        print("✅ Configuration initiale de la base de données terminée.")
        return True
    else:
        print("✅ La base de données existe déjà.")
        return True

def reset_db(app):
    """Réinitialise la base de données (pour le développement uniquement)"""
    print("🔄 Réinitialisation de la base de données...")

    db_path = os.path.join(app.root_path, 'hbnb.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("✅ Ancienne base de données supprimée.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de la base: {str(e)}")
            return False

    return init_db(app)

if __name__ == "__main__":
    import sys
    app = create_app()

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        if reset_db(app):
            print("✅ Base de données réinitialisée avec succès.")
        else:
            print("❌ Échec de la réinitialisation de la base de données.")
            sys.exit(1)
    else:
        if init_db(app):
            print("✅ Initialisation de la base de données terminée.")
        else:
            print("❌ Échec de l'initialisation de la base de données.")
            sys.exit(1)
