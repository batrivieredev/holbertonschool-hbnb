#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'  # ✅ Define table name

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Amenity {self.name}>"
