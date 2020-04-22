#!/usr/bin/python3
"""This is the DB storage class for AirBnB"""
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session


class DBStorage:
    """Represents a database storage engine.

    Arguments:
        __engine (sqlalchemy.Engine):  SQLAlchemy engine.
        __session (sqlalchemy.Session): SQLAlchemy session.
    """
    __engine = None
    __session = None
    __mdoels = ["State", "City", "User", "Place", "Review", "Amenity"]

    def __init__(self):
        """
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user,
                                                 pwd,
                                                 host,
                                                 db), pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """add the object to the current database session .

        Arguments:
            obj (object) Model instance object
        """
        self.__session.add(obj)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name cls

        Arguments:
            cls (str) Model instance class name
        """
        if cls is None:
            objs = []
            for obj in self.__mdoels:
                objs.extend(self.__session.query(eval(obj)).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(obj).__name__,
                               obj.id): obj for obj in objs}

    def save(self):
        """commit all changes of the current database session

        Arguments:
            None
        """
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None

        Arguments:
            obj (object) Model instance object
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)
        and create the current database sessions

        Arguments:
            None
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """close the current database session

        Arguments
            None
        """
        self.__session.close()
