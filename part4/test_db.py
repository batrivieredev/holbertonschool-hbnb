import os
from app import create_app
from app.extensions import db

def test_db_connection():
    """Test database connection and write permissions."""
    print("🔍 Testing database connection...")

    # Get database path
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hbnb.db')
    print(f"📁 Database path: {db_path}")

    # Check directory permissions
    dir_path = os.path.dirname(db_path)
    if os.access(dir_path, os.W_OK):
        print(f"✅ Directory {dir_path} is writable")
    else:
        print(f"❌ Directory {dir_path} is not writable")

    # Try to create app and connect to database
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            # Try to write to database
            db.session.execute('SELECT 1')
            db.session.commit()
        print("✅ Successfully connected to and wrote to database")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_db_connection()
    if success:
        print("🎉 All database tests passed!")
    else:
        print("❌ Database tests failed!")
