#!/usr/bin/env python3
"""model - storage engine model"""

import json
from datetime import datetime
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        with open(FileStorage.__file_path, mode="w", encoding="utf-8") as f:
            json_str = json.dumps(FileStorage.__objects,
                                  defualt=lambda obj: obj.to_dict())
            f.write(json_str)

    def reload(self):
        try:
            with open(FileStorage.__file_path, encoding="utf-8") as f:
                FileStorage.__objects = json.loads(f.read(),
                                                   object_hook=self.
                                                   json_to_python)
        except FileNotFoundError:
            pass