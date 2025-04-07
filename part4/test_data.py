from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def init_test_data():
    app = create_app()
    with app.app_context():
        # Vérifier et créer les utilisateurs de test
        admin_email = "admin@hbnb.io"
        test_email = "test@example.com"

        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                password=bcrypt.generate_password_hash("admin123").decode('utf-8'),
                first_name="Admin",
                last_name="User",
                is_admin=True
            )
            db.session.add(admin)

        user1 = User.query.filter_by(email=test_email).first()
        if not user1:
            user1 = User(
                email=test_email,
                password=bcrypt.generate_password_hash("test123").decode('utf-8'),
                first_name="Test",
                last_name="User"
            )
            db.session.add(user1)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création des utilisateurs: {e}")
            return

        # Créer les logements de test
        if not Place.query.first():
            places = [
                Place(
                    title="Appartement lumineux au centre-ville",
                    description="Bel appartement rénové avec vue sur la ville",
                    price=150.0,
                    latitude=48.8566,
                    longitude=2.3522,
                    owner_id=user1.id
                ),
                Place(
                    title="Villa avec piscine",
                    description="Magnifique villa avec piscine et jardin",
                    price=300.0,
                    latitude=43.2965,
                    longitude=5.3698,
                    owner_id=user1.id
                ),
                Place(
                    title="Studio cosy",
                    description="Studio confortable près des transports",
                    price=80.0,
                    latitude=45.7578,
                    longitude=4.8320,
                    owner_id=user1.id
                )
            ]

            db.session.add_all(places)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Erreur lors de la création des logements: {e}")
                return

            # Créer les avis test
            reviews = [
                Review(
                    text="Très bon séjour, je recommande !",
                    rating=5,
                    place_id=places[0].id,
                    user_id=user1.id
                ),
                Review(
                    text="Bien situé mais un peu bruyant",
                    rating=4,
                    place_id=places[0].id,
                    user_id=admin.id
                )
            ]

            db.session.add_all(reviews)
            try:
                db.session.commit()
                print("✅ Données de test insérées avec succès")
            except Exception as e:
                db.session.rollback()
                print(f"Erreur lors de la création des avis: {e}")
                return

if __name__ == '__main__':
    init_test_data()
