from app.extensions import db
from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    """Amenity model for storing place amenities."""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), unique=True, nullable=False, index=True)

    def validate(self):
        """Validate amenity attributes."""
        if not self.name or len(self.name) > 50:
            raise ValueError("Name is required and must be less than 50 characters")

        # Check name uniqueness
        existing_amenity = Amenity.query.filter(
            Amenity.name == self.name,
            Amenity.id != self.id
        ).first()
        if existing_amenity:
            raise ValueError("Amenity name already exists")

    def to_dict(self):
        """Convert the amenity instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_amenity(data):
        """Create a new amenity."""
        amenity = Amenity(name=data['name'])
        amenity.validate()
        amenity.save()
        return amenity

    def update_from_dict(self, data):
        """Update amenity attributes from a dictionary."""
        if 'name' in data:
            self.name = data['name']
            self.validate()
            self.save()

    @classmethod
    def get_by_name(cls, name):
        """Get amenity by name."""
        return cls.query.filter_by(name=name).first()

    def __repr__(self):
        return f"<Amenity {self.name}>"

    def __str__(self):
        return self.name
