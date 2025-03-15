import os
from app import create_app
from sqlalchemy import create_engine, text

DB_NAME = "hbnb_db"
SQL_SCRIPT_PATH = "hbnb_schema.sql"

def reset_database():
    """Vérifie et recrée la base de données si elle n'existe pas."""
    
    # 📌 Connexion directe à MySQL sans base
    engine = create_engine("mysql+pymysql://debian-sys-maint:fB33r9vNp0V8hA8M@localhost/")

    with engine.connect() as connection:
        try:
            # Vérifier si la base existe
            result = connection.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}';"))
            db_exists = result.fetchone()

            if not db_exists:
                print(f"🔄 La base {DB_NAME} n'existe pas, création en cours...")
                connection.execute(text(f"CREATE DATABASE {DB_NAME};"))
                print(f"✅ Base de données {DB_NAME} créée.")

        except Exception as e:
            print(f"❌ ERREUR LORS DE LA CRÉATION DE LA BASE : {e}")
            return

    # 📌 Maintenant, on peut attacher Flask à la base et exécuter le script SQL
    app = create_app()
    with app.app_context():
        with app.extensions['sqlalchemy'].engine.connect() as connection:
            print(f"🔄 Exécution du script SQL sur {DB_NAME}...")
            try:
                with open(SQL_SCRIPT_PATH, "r") as sql_file:
                    sql_commands = sql_file.read().split(";")
                for command in sql_commands:
                    if command.strip():
                        connection.execute(text(command))
                print("✅ Base de données initialisée avec succès.")
            except Exception as e:
                print(f"❌ ERREUR LORS DE L'EXÉCUTION DU SCRIPT SQL : {e}")

if __name__ == "__main__":
    reset_database()
