#!/usr/bin/env python3
"""Script de création de l'utilisateur administrateur"""
from app import create_app
from app.extensions import db
from app.models.user import User

def create_admin():
    """Crée un utilisateur administrateur s'il n'existe pas"""
    print("🔄 Création de l'utilisateur administrateur...")

    try:
        app = create_app()
        with app.app_context():
            # Vérifie si l'admin existe déjà
            existing_admin = User.query.filter_by(email='admin@hbnb.io').first()

            if existing_admin:
                print("ℹ️ L'administrateur existe déjà")
                return True

            # Création de l'administrateur
            admin = User(
                first_name='Admin',
                last_name='HBNB',
                email='admin@hbnb.io',
                is_admin=True
            )
            # Définition du mot de passe
            admin.hash_password('admin12345')

            # Sauvegarde en base de données
            db.session.add(admin)
            db.session.commit()

            print("✅ Administrateur créé avec succès!")
            print("\nIdentifiants de connexion:")
            print("📧 Email: admin@hbnb.io")
            print("🔑 Mot de passe: admin12345")
            return True

    except Exception as e:
        print(f"❌ Erreur lors de la création de l'administrateur: {str(e)}")
        if 'db' in locals():
            db.session.rollback()
        return False

if __name__ == "__main__":
    if create_admin():
        print("✅ Création de l'administrateur terminée.")
    else:
        import sys
        print("❌ Échec de la création de l'administrateur.")
        sys.exit(1)
