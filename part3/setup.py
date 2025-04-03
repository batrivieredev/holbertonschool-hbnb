import os
from app import create_app
from sqlalchemy import text
from app.models.user import User
from app.extensions import db, bcrypt

SQL_SCRIPT_PATH = "hbnb_schema.sql"

def reset_database():
    """Réinitialise la base de données SQLite."""
    print("🔄 Réinitialisation de la base de données SQLite...")
    db_path = os.getenv("DATABASE_URL", "sqlite:///hbnb.db").replace("sqlite:///", "")

    # Supprimer l'ancienne base de données si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Base de données supprimée : {db_path}")

    app = create_app()
    with app.app_context():
        db.create_all()  # Crée les tables définies dans les modèles
        print("✅ Tables créées avec succès.")

        # Exécuter le script SQL pour insérer des données initiales
        try:
            with open(SQL_SCRIPT_PATH, "r") as sql_file:
                sql_commands = sql_file.read().split(";")
                for command in sql_commands:
                    if command.strip():
                        db.session.execute(text(command.strip()))
                db.session.commit()
            print("✅ Données initiales insérées avec succès.")
        except Exception as e:
            print(f"❌ ERREUR LORS DE L'EXÉCUTION DU SCRIPT SQL : {e}")

def create_admin():
    """Ajoute un administrateur si inexistant avec un mot de passe hashé."""
    print("🔄 Initialisation de l'admin...")
    app = create_app()
    with app.app_context():
        existing_admin = User.query.filter_by(email="admin@hbnb.io").first()
        if existing_admin:
            print(f"✅ Admin déjà présent : {existing_admin.email}")
            return

        hashed_password = bcrypt.generate_password_hash("admin12345").decode("utf-8")
        admin = User(
            id="37c9050e-ddd3-4c3b-9731-9f487208bbc2",
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin créé avec succès !")
