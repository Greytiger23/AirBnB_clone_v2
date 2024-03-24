#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import models

association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"), primary_key=True),
                          Column("amenity_id", String(60), ForeignKey(
                                 "amenities.id"), primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", cascade='all, delete', backref="place")
    amenities = relationship("Amenity", secondary=association_table,
                              viewonly=False,
                              back_populates="association_table")

    def __init__(self, *args, **kwargs):
        """initialize a place object"""
        super().__init__(*args, **kwargs)
        self.amenity_ids = []

    def reviews(self):
        """stores the reviews"""
        from models import storage
        from models.review import Review
        r = models.storage.all(Review)
        return [review for review in r.values() if review.place_id == self.id]

    def amenities(self):
        """property getter for amenities"""
        from models import storage
        from models.amenity import Amenity
        a = models.storage.all(Amenity)
        return [amenity for amenity in a.values() if amenity.id in
                self.amenity_ids]

    def amenities(self, amenity_obj):
        """setter for amenities"""
        if isinstance(amenity_obj, Amenity):
            self.amenity_ids.append(amenity_obj.id)
