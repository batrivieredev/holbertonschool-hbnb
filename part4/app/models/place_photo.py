from app.extensions import db
from app.models.BaseModel import BaseModel

class PlacePhoto(BaseModel):
    """Model for storing place photos."""

    __tablename__ = 'place_photos'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(100))
    is_primary = db.Column(db.Boolean, default=False)

    # Relationship
    place = db.relationship('Place', back_populates='photos')

    def to_dict(self):
        """Convert the photo instance to a dictionary."""
        photo_dict = super().to_dict()
        photo_dict.update({
            'photo_url': self.photo_url,
            'caption': self.caption,
            'is_primary': self.is_primary
        })
        return photo_dict

    def __repr__(self):
        return f"<PlacePhoto {self.photo_url}>"
