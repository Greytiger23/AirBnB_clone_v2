#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
