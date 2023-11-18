#!/usr/bin/python3
""" Members Monthly contribution"""
from datetime import datetime
from models.base_model import BaseModel, Base
from models.base_model import BaseModel, Base
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import  Optional



class Logs(BaseModel, Base):
    """table representing member's monthly contribution"""
    __tablename__ = "log"
    
    member_id: Mapped[str] = mapped_column(ForeignKey('users_profile.id'), nullable=False)
    amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow())



    # write a logic to accept contributions in multiple of 10K

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)