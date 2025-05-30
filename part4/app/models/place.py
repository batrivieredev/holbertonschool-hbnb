from app.extensions import db
from app.models.BaseModel import BaseModel

# Place-Amenity association table with explicit foreign keys
place_amenity = db.Table('place_amenities',
    db.Column('place_id', db.String(36),
              db.ForeignKey('places.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('amenity_id', db.String(36),
              db.ForeignKey('amenities.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('created_at', db.DateTime, server_default=db.func.now()),
    db.Column('updated_at', db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
)

class Place(BaseModel):
    """Place model for storing location data."""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', backref='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete')
    photos = db.relationship('PlacePhoto', back_populates='place', cascade='all, delete')
    amenities = db.relationship('Amenity',
                               secondary=place_amenity,
                               lazy='dynamic',
                               cascade='all, delete',
                               backref=db.backref('places', lazy='dynamic'))

    def validate(self):
        """Validate place attributes."""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be less than 100 characters")

        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a positive number")

        if not isinstance(self.latitude, (int, float)) or self.latitude < -90 or self.latitude > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")

        if not isinstance(self.longitude, (int, float)) or self.longitude < -180 or self.longitude > 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")

    def to_dict(self):
        """Convert the place instance to a dictionary."""
        place_dict = super().to_dict()

        # Add owner information
        if self.owner:
            place_dict['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }

        # Add reviews
        place_dict['reviews'] = [review.to_dict() for review in self.reviews] if self.reviews else []

        # Add photos
        place_dict['photos'] = [photo.to_dict() for photo in self.photos] if self.photos else []

        # Add amenities
        place_dict['amenities'] = [amenity.to_dict() for amenity in self.amenities.all()] if self.amenities else []

        return place_dict

    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def remove_review(self, review):
        """Remove a review from the place."""
        if review in self.reviews:
            self.reviews.remove(review)
            self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities.all():
            self.amenities.append(amenity)
            self.save()

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities.all():
            self.amenities.remove(amenity)
            self.save()

    def update_from_dict(self, data):
        """Update place attributes from a dictionary."""
        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for field in allowed_fields:
            if field in data:
                setattr(self, field, data[field])

        # Handle photos
        if 'photos' in data and isinstance(data['photos'], list):
            from app.models.place_photo import PlacePhoto
            # Update existing photos
            for photo_data in data['photos']:
                if 'id' in photo_data:
                    photo = PlacePhoto.query.get(photo_data['id'])
                    if photo and photo.place_id == self.id:
                        photo.photo_url = photo_data.get('photo_url', photo.photo_url)
                        photo.caption = photo_data.get('caption', photo.caption)
                        photo.is_primary = photo_data.get('is_primary', photo.is_primary)
                else:
                    # Add new photo
                    photo = PlacePhoto(
                        place_id=self.id,
                        photo_url=photo_data['photo_url'],
                        caption=photo_data.get('caption'),
                        is_primary=photo_data.get('is_primary', False)
                    )
                    self.photos.append(photo)

        # Handle amenities
        if 'amenities' in data and isinstance(data['amenities'], list):
            from app.models.amenity import Amenity
            current_amenities = list(self.amenities)
            for amenity in current_amenities:
                self.amenities.remove(amenity)

            for amenity_id in data['amenities']:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    self.amenities.append(amenity)

        self.validate()
        self.save()

    @staticmethod
    def create_place(data, owner_id):
        """Create a new place."""
        place = Place(
            title=data['title'],
            description=data.get('description'),
            price=float(data['price']),
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            owner_id=owner_id
        )
        place.validate()
        place.save()

        # Handle photos
        if 'photos' in data and isinstance(data['photos'], list):
            from app.models.place_photo import PlacePhoto
            for photo_data in data['photos']:
                photo = PlacePhoto(
                    place_id=place.id,
                    photo_url=photo_data['photo_url'],
                    caption=photo_data.get('caption'),
                    is_primary=photo_data.get('is_primary', False)
                )
                place.photos.append(photo)

        # Handle amenities
        if 'amenities' in data and isinstance(data['amenities'], list):
            from app.models.amenity import Amenity
            for amenity_id in data['amenities']:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
            place.save()

        return place
def is_available(self, start_date, end_date):
    """Vérifie si le logement est disponible pour une période donnée."""
    from app.models.booking import Booking
    return not Booking.query.filter(
        Booking.place_id == self.id,
        Booking.status == 'confirmed',
        ((Booking.start_date <= end_date) & (Booking.end_date >= start_date))
    ).first()

def get_booked_periods(self):
    """Retourne les périodes où le logement est réservé."""
    from app.models.booking import Booking
    return Booking.query.filter(
        Booking.place_id == self.id,
        Booking.status == 'confirmed'
    ).order_by(Booking.start_date).all()

def to_dict(self):
    """Convert the place instance to a dictionary."""
    place_dict = super().to_dict()

    # Add booked periods
    place_dict['booked_periods'] = [{
        'start_date': booking.start_date.isoformat(),
        'end_date': booking.end_date.isoformat()
    } for booking in self.get_booked_periods()]

    # Add owner information
    if self.owner:
        place_dict['owner'] = {
            'id': self.owner.id,
            'first_name': self.owner.first_name,
            'last_name': self.owner.last_name,
            'email': self.owner.email
        }

    # Add reviews
    place_dict['reviews'] = [review.to_dict() for review in self.reviews] if self.reviews else []

    # Add photos
    place_dict['photos'] = [photo.to_dict() for photo in self.photos] if self.photos else []

    # Add amenities
    place_dict['amenities'] = [amenity.to_dict() for amenity in self.amenities.all()] if self.amenities else []

    return place_dict

def __repr__(self):
    return f"<Place {self.title}>"

