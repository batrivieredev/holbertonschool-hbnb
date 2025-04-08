import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(db.Model):
    """Base model class that includes UUID and timestamp attributes."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Generate __tablename__ automatically from class name."""
        return cls.__name__.lower() + 's'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize with UUID and timestamps if not provided."""
        if not 'id' in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        if not 'created_at' in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if not 'updated_at' in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        super().__init__(*args, **kwargs)

    def save(self):
        """Save the current instance and update timestamps."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the current instance."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        """Update instance attributes and save changes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert instance to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    @classmethod
    def get_by_id(cls, id):
        """Get instance by ID."""
        return cls.query.get(str(id))

    @classmethod
    def get_all(cls):
        """Get all instances."""
        return cls.query.all()

    def validate(self):
        """
        Base validation method to be overridden by child classes.
        Should raise ValueError if validation fails.
        """
        pass

    def __repr__(self):
        """Return string representation of the instance."""
        return f"<{self.__class__.__name__} {self.id}>"
