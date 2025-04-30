#!/usr/bin/env python3
"""Script d'initialisation de la base de données"""
import os
from app import create_app
from app.extensions import db, init_db_events
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place_photo import PlacePhoto

def create_sample_data():
    """Crée des données d'exemple pour la base de données"""
    try:
        # Création de quelques utilisateurs propriétaires
        owners = [
            User(
                first_name="Jean",
                last_name="Dupont",
                email="jean.dupont@example.com",
                is_admin=False
            ),
            User(
                first_name="Marie",
                last_name="Martin",
                email="marie.martin@example.com",
                is_admin=False
            ),
            User(
                first_name="Pierre",
                last_name="Bernard",
                email="pierre.bernard@example.com",
                is_admin=False
            )
        ]

        for owner in owners:
            owner.hash_password('password123')
            db.session.add(owner)

        # Récupération des équipements pour les associer aux places
        amenities = Amenity.query.all()

        # Création des places
        places = [
            {
                "name": "Villa avec piscine",
                "description": "Magnifique villa avec piscine privée et jardin",
                "number_rooms": 4,
                "number_bathrooms": 2,
                "max_guest": 8,
                "price_by_night": 250,
                "latitude": 43.610769,
                "longitude": 3.876716,
                "city": "Montpellier",
                "owner": owners[0],
                "amenities": amenities[:5]  # 5 premiers équipements
            },
            {
                "name": "Appartement centre-ville",
                "description": "Charmant appartement en plein cœur de Paris",
                "number_rooms": 2,
                "number_bathrooms": 1,
                "max_guest": 4,
                "price_by_night": 150,
                "latitude": 48.856614,
                "longitude": 2.352222,
                "city": "Paris",
                "owner": owners[1],
                "amenities": amenities[2:7]  # 5 équipements différents
            },
            {
                "name": "Maison de campagne",
                "description": "Maison traditionnelle au calme avec grand terrain",
                "number_rooms": 3,
                "number_bathrooms": 2,
                "max_guest": 6,
                "price_by_night": 180,
                "latitude": 45.764043,
                "longitude": 4.835659,
                "city": "Lyon",
                "owner": owners[2],
                "amenities": amenities[5:]  # derniers équipements
            }
        ]

        for place_data in places:
            place = Place(
                name=place_data["name"],
                description=place_data["description"],
                number_rooms=place_data["number_rooms"],
                number_bathrooms=place_data["number_bathrooms"],
                max_guest=place_data["max_guest"],
                price_by_night=place_data["price_by_night"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                city=place_data["city"],
                owner=place_data["owner"]
            )
            place.amenities.extend(place_data["amenities"])
            db.session.add(place)

        db.session.commit()
        print("✅ Données d'exemple créées avec succès.")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors de la création des données d'exemple: {str(e)}")
        return False

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

        # Création des données d'exemple
        if create_sample_data():
            print("✅ Données d'exemple ajoutées à la base de données.")
        else:
            print("⚠️ Échec de la création des données d'exemple.")

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
