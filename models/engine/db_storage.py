#!/usr/bin/python3
"""module that defines the DBStorage class"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.user import User
from sqlalchemy.ext.declarative import declarative_base


class DBStorage:
    """represents the DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """public instance method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in database"""
        a = {}
        classes = [User, State, City, Amenity, Place, Review]
        if cls:
            classes = [cls]
        for c in classes:
            b = self.__session.query(c)
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
            self.session.delete(obj)

    def reload(self):
        """Create all tables in the database and current database session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """closes the session"""
        self.__session.close()
