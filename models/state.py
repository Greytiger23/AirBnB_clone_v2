#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
import models
import shlex
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan",
                          backref="state")

    def cities(self):
        """represents the city"""
        a = models.storage.all()
        b = []
        x = []
        for key in a:
            c = key.replace('.', ' ')
            c = shlex.split(c)
            if (c[0] == 'City'):
                lista.append(a[key])
        for y in b:
            if (y.state_id == self.id):
                x.append(y)
        return x


    if storage_type != 'db':
        def cities(self):
            """getter method to the list of city"""
            from models import storage
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
