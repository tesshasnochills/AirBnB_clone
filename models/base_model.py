#!/usr/bin/env python3
"""model - base model"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """base class for hbnb"""
    id = None
    updated_at = None
    created_at = None

    def __init__(self, *args, **kwargs):
        """initialization of base model variables"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)

            if "created_at" in kwargs:
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")

            if "updated_at" in kwargs:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """str function to return class name id and dictionary"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """updates 'updated_at' instance with current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """dict function to return the created dictionary"""
        dict_obj = self.__dict__.copy()
        dict_obj["__class__"] = self.__class__.__name__
        dict_obj["created_at"] = self.created_at.isoformat()
        dict_obj["updated_at"] = self.updated_at.isoformat()
        return dict_obj
