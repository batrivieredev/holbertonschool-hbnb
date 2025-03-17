from app.extensions import db
from app.models.BaseModel import BaseModel
from app.models.user import User  # ✅ Import User model
from sqlalchemy.dialects.mysql import CHAR
import uuid

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    # ✅ Add relationship to User model
    owner = db.relationship('User', backref='places')

    # ✅ Existing relationships
    amenities = db.relationship('Amenity', backref='place', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete')

    def to_dict(self):
        """Convert model instance to dict."""
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            } if self.owner else None,  # ✅ Include owner details
            'amenities': [amenity.to_dict() for amenity in self.amenities] if self.amenities else [],
            'reviews': [review.to_dict() for review in self.reviews] if self.reviews else []
        }

    def __repr__(self):
        return f"<Place {self.title}>"
