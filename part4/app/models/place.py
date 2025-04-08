from app.extensions import db
from app.models.BaseModel import BaseModel
from app.models.user import User

class Place(BaseModel):
    """Représente un lieu dans la base de données."""
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # ✅ Add relationship to User model
    owner = db.relationship('User', backref='places')

    # ✅ Existing relationships
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete')

    def to_dict(self):
        """Convert model instance to dict."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            } if self.owner else None,
            'reviews': [review.to_dict() for review in self.reviews] if self.reviews else []
        }

    def __repr__(self):
        return f"<Place {self.title}>"
