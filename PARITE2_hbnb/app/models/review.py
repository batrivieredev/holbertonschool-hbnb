#!/usr/bin/python3

from app.models.BaseModel import BaseModel


class Review(BaseModel):
    def __init__(self, place_id, user_id, text, rating, place=None, user=None):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
