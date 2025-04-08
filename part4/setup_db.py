import os
from app import create_app
from sqlalchemy import text
from app.models.user import User
from app.extensions import db, bcrypt

def ensure_app_directory():
    """Create app directory if it doesn't exist and ensure it's writable."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(current_dir, exist_ok=True)
    print(f"✅ Directory ready at {current_dir}")
    return current_dir

def init_database():
    """Initialize the database if it doesn't exist."""
    print("🔄 Checking database...")
    db_dir = ensure_app_directory()
    db_file = os.path.join(db_dir, 'hbnb.db')

    app = create_app()
    with app.app_context():
        if not os.path.exists(db_file):
            print("📁 Creating new database...")
            db.create_all()
            print("✅ Tables created successfully.")

            # Execute SQL script for initial setup if needed
            try:
                with open('hbnb_schema.sql', 'r') as sql_file:
                    sql_commands = sql_file.read().split(";")
                    for command in sql_commands:
                        if command.strip():
                            db.session.execute(text(command.strip()))
                    db.session.commit()
                print("✅ Initial database setup completed.")
            except Exception as e:
                print(f"❌ Error during SQL script execution: {e}")
        else:
            print("✅ Database already exists.")

def reset_database():
    """Reset the database (only when explicitly called)."""
    print("🔄 Resetting database...")
    db_dir = ensure_app_directory()
    db_file = os.path.join(db_dir, 'hbnb.db')

    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"🗑️ Old database removed: {db_file}")

    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tables created successfully.")

            with open('hbnb_schema.sql', 'r') as sql_file:
                sql_commands = sql_file.read().split(";")
                for command in sql_commands:
                    if command.strip():
                        db.session.execute(text(command.strip()))
                db.session.commit()
            print("✅ Database reset completed.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during database setup: {e}")
            raise

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        init_database()
