#!/usr/bin/python3
""" User Model for Project """
from models.base_model import BaseModel, Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from utils import hash_password


class User(BaseModel, Base):
    """ User Class """
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(
        String(60), nullable=False)
    reset_token: Mapped[Optional[str | None]] = mapped_column(String(60), nullable=True)   

    # Relationships
    user_profile: Mapped["UserProfile"] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """
            instantiation of new User Class
        """
        if kwargs:
            if 'password' in kwargs:
                hashed_pwd = hash_password(kwargs['password'])
                kwargs['password'] = hashed_pwd
        super().__init__(*args, **kwargs)
