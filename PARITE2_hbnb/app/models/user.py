#!/usr/bin/env python3

from app.models.BaseModel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]  # Limit max length
        self.last_name = last_name[:50]  # Limit max length
        self.email = email  # Validate email externally
        self.is_admin = is_admin
