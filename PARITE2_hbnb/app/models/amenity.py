#!/usr/bin/env python3

from app.models.BaseModel import BaseModel
class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name[:50]
