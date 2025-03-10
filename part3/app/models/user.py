#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel

class User(BaseModel):
    __tablename__ = 'users'  # ✅ Define table name

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
