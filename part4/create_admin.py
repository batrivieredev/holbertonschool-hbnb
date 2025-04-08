from app import create_app
from app.models.user import User
from app.extensions import db

def create_admin():
    """Create an admin user if it doesn't exist."""
    print("🔄 Creating admin user...")

    app = create_app()
    with app.app_context():
        try:
            # Check if admin already exists
            existing_admin = User.query.filter_by(email='admin@hbnb.io').first()
            if existing_admin:
                print("ℹ️  Admin user already exists")
                print("📧 Email: admin@hbnb.io")
                print("🔑 Password: admin12345")
                return

            # Create new admin if it doesn't exist
            admin = User(
                first_name='Admin',
                last_name='HBnB',
                email='admin@hbnb.io',
                is_admin=True
            )
            admin.hash_password('admin12345')

            db.session.add(admin)
            db.session.commit()

            print("✅ Admin user created successfully!")
            print("\nLogin credentials:")
            print("📧 Email: admin@hbnb.io")
            print("🔑 Password: admin12345")

        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    create_admin()
