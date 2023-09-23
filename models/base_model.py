#!/usr/bin/python3
""" Base Model for other models to be used in this project """
from datetime import datetime
import json
import models
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Any
import uuid


# format for datetime
time_format = "%Y-%m-%dT%H:%M:%S.%f"

# Base from sqlalchemy


class Base(DeclarativeBase):
    pass


class BaseModel:
    """ Base class for other classes in this project """
    id: Mapped[str] = mapped_column(
        String(60), nullable=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
            instantiation of new BaseModel Class
        """
        if kwargs:
            self.__set_attrs(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __set_attrs(self, attr_dict: dict) -> None:
        """ set attributes """
        if "id" not in attr_dict:
            attr_dict['id'] = str(uuid.uuid4())
        if "created_at" not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif "created_at" in attr_dict and type(attr_dict["created_at"]) is str:
            attr_dict['.created_at'] = datetime.strptime(
                attr_dict["created_at"], time_format)
        if "updated_at" not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif "updated_at" in attr_dict and type(attr_dict["updated_at"]) is str:
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict["updated_at"], time_format)
        if "__class__" in attr_dict:
            del attr_dict["__class__"]
        for key, value in attr_dict.items():
            setattr(self, key, value)

    def __is_serializable(self, obj: Any) -> bool:
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def to_dict(self) -> dict:
        """
            returns a dictionary containing all keys/values of __dict__ of the instance
        """
        obj_class = self.__class__.__name__
        dict_obj = {}
        for key, value in self.__dict__.items():
            if self.__is_serializable(value):
                dict_obj[key] = value
            else:
                dict_obj[key] = str(value)  # convert to string
            if isinstance(value, datetime):
                dict_obj[key] = value.strftime(time_format)
        dict_obj["__class__"] = obj_class
        dict_obj.pop('_sa_instance_state', None)
        if obj_class == 'User':
            dict_obj.pop('password', None)
        return dict_obj

    def save(self):
        """Add an object in the DB """
        self.updated_at = datetime.utcnow()  # update time of operation
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Delete an instance from the DB"""
        models.storage.delete(self)

    def update(self, dict_obj: dict = None):
        """Update a model"""
        IGNORE = [
            'id', 'created_at', 'updated_at', 'email',
            'user_id', 'loan_id', 'guarantor_id', 'member_id'
        ]
        if dict_obj:
            updated_dict = {
                key: value for key, value in dict_obj.items() if key not in IGNORE
            }
            if '__class__' in updated_dict:
                del updated_dict['__class__']
            for key, value in updated_dict.items():
                setattr(self, key, value)
            self.save()

    def __str__(self) -> str:
        """ string representation of BaseModel """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
