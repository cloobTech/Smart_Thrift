#!/usr/bin/python3
""" User Class for Project """
from models.base_model import BaseModel, Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from utils import hash_password


class User(BaseModel, Base):
    """ User Class """
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[str] = mapped_column(String(60), nullable=False, default='member')
    slot: Mapped[int] = mapped_column(nullable=False, default=1)
    registered: Mapped[bool] = mapped_column(nullable=False, default=True)
    reset_token: Mapped[Optional[str]]

    # Relationships
    loan_out: Mapped[list["LoanOut"]] = relationship(back_populates='member')
    contribution: Mapped[list["Contribution"]] = relationship(back_populates='member')

    def __init__(self, *args, **kwargs):
        """
            instantiation of new User Class
        """
        if kwargs:
            if 'password' in kwargs:
                hashed_pwd = hash_password(kwargs['password'])
                kwargs['password'] = hashed_pwd
        super().__init__(*args, **kwargs)
