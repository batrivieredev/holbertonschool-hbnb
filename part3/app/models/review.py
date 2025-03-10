#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'  # ✅ Define table name

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place = db.relationship('Place', backref='reviews', lazy=True)  # ✅ Define relationship
    user = db.relationship('User', backref='reviews', lazy=True)  # ✅ Define relationship

    def __repr__(self):
        return f"<Review {self.rating}/5 for Place {self.place_id}>"
