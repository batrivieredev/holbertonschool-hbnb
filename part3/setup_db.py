import os
from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity  # ✅ Vérifier l'import des modèles
from sqlalchemy import inspect

DB_PATH = "hbnb.db"

def reset_database():
    """Supprime l'ancienne base de données et recrée une nouvelle."""
    if os.path.exists(DB_PATH):
        print("🔄 Suppression de l'ancienne base de données...")
        os.remove(DB_PATH)
    else:
        print("✅ Aucune base existante, création d'une nouvelle...")

    # Créer l'application Flask et initialiser la base
    app = create_app()
    with app.app_context():
        print("🔄 Création des tables en cours...")
        try:
            print("📌 URL de la base de données utilisée:", db.engine.url)
            db.create_all()  # ✅ Création des tables
            print("📌 Colonnes de la table users :", db.metadata.tables["users"].columns.keys())
            print("📌 Modèles SQLAlchemy détectés :", db.metadata.tables.keys())
            print("✅ Base de données créée avec succès !")

            # Vérification des tables créées
            inspector = inspect(db.engine)
            print("📌 Tables détectées après création:", inspector.get_table_names())

        except Exception as e:
            print("❌ ERREUR LORS DE LA CRÉATION DES TABLES :", e)

def clean_database():
    """Supprime toutes les données des tables sans supprimer la structure."""
    app = create_app()
    with app.app_context():
        try:
            print("🧹 Nettoyage de la base de données en cours...")
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print(f"🗑 Suppression des données de {table.name}...")
                db.session.execute(table.delete())  # ✅ Supprime les données mais garde les tables
            db.session.commit()
            print("✅ Base de données nettoyée avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage de la base de données : {e}")
            db.session.rollback()


if __name__ == "__main__":
    reset_database()
