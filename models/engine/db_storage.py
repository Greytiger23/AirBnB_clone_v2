#!/usr/bin/python3
"""module that defines the DBStorage class"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import *


class DBStorage:
    """represents the DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """public instance method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in database"""
        a = {}
        classes = [User, State, City, Amenity, Place, Review]
        if cls:
            classes = [cls]
        for c in classes:
            b = self.__session.query(c).all()
            for obj in b:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                a[key] = obj
        return a

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and current database session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
