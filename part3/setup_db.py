import os
from app import create_app
from sqlalchemy import create_engine, text
from app.models.user import User
from app.extensions import db, bcrypt  # ✅ Ajout de bcrypt

DB_NAME = "hbnb_db"
SQL_SCRIPT_PATH = "hbnb_schema.sql"

def reset_database():
    """Vérifie et recrée la base de données si elle n'existe pas."""
    print("🔄 Suppression et recréation de la base de données...")
    engine = create_engine("mysql+pymysql://debian-sys-maint:fB33r9vNp0V8hA8M@localhost/")

    with engine.connect() as connection:
        try:
            result = connection.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}';"))
            db_exists = result.fetchone()

            if not db_exists:
                print(f"🔄 La base {DB_NAME} n'existe pas, création en cours...")
                connection.execute(text(f"CREATE DATABASE {DB_NAME};"))
                print(f"✅ Base de données {DB_NAME} créée.")

        except Exception as e:
            print(f"❌ ERREUR LORS DE LA CRÉATION DE LA BASE : {e}")
            return

    app = create_app()
    with app.app_context():
        with app.extensions['sqlalchemy'].engine.connect() as connection:
            print(f"🔄 Exécution du script SQL sur {DB_NAME}...")
            try:
                with open(SQL_SCRIPT_PATH, "r") as sql_file:
                    sql_commands = sql_file.read().split(";")

                for command in sql_commands:
                    if command.strip():
                        print(f"📌 Exécution : {command.strip()}")  
                        result = connection.execute(text(command.strip()))
                        print(f"✅ Résultat exécution : {result}")

                admin_check = connection.execute(text("SELECT * FROM users WHERE email='admin@hbnb.io'")).fetchone()
                if admin_check:
                    print("✅ L'utilisateur admin a bien été inséré dans la base de données.")
                else:
                    print("❌ L'utilisateur admin n'a PAS été inséré correctement !")

                print("✅ Base de données initialisée avec succès.")

            except Exception as e:
                print(f"❌ ERREUR LORS DE L'EXÉCUTION DU SCRIPT SQL : {e}")

def create_admin():
    """Ajoute un administrateur si inexistant avec un mot de passe hashé."""
    print("🔄 Initialisation de l'admin...")
    app = create_app()
    with app.app_context():
        print("🔄 Vérification de l'admin dans la base de données...")
        existing_admin = User.query.filter_by(email="admin2@hbnb.io").first()
        print(f"📌 Admin existant : {existing_admin}")
        if existing_admin:
            print(f"✅ Admin déjà présent : {existing_admin.email}")
            return

        print("🔄 Création de l'admin via SQLAlchemy...")
        hashed_password = bcrypt.generate_password_hash("admin12345").decode("utf-8")  # ✅ Hash du mot de passe

        admin = User(
            id="37c9050e-ddd3-4c3b-9731-9f487208bbc2",
            first_name="Admin2",
            last_name="HBnB0",
            email="admin2@hbnb.io",
            password=hashed_password,  # ✅ On stocke le mot de passe hashé
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()  # ✅ IMPORTANT : Commit des changements
        print("✅ Admin créé avec succès via SQLAlchemy !")

        # Vérification après insertion
        admin_check = User.query.filter_by(email="admin@hbnb.io").first()
        if admin_check:
            print("✅ L'admin est bien présent après insertion !")
        else:
            print("❌ L'admin n'apparaît toujours pas après insertion !")


if __name__ == "__main__":
    reset_database()
    create_admin()
