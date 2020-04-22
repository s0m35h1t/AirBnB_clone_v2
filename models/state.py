#!/usr/bin/python3
"""This is the state class"""
import models
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        __tablename__ (str): The name of the MySQL table to store States.
        name (orm String): State name.
        cities (orm relationship): The State-City relationship.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="all,delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get related City objects."""
            cities = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    cities.append(city)
            return cities
