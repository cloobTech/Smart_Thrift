#!/usr/bin/python3
""" Members Monthly contribution"""
from datetime import datetime
from models.base_model import BaseModel, Base
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import  Optional



class Contribution(BaseModel, Base):
    """table representing member's monthly contribution"""
    __tablename__ = "contributions"
    
    member_id: Mapped[str] = mapped_column(ForeignKey('users_profile.id'), nullable=False)
    amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow())
    advance_month: Mapped[int] = mapped_column(nullable=True, default=0)
    slot: Mapped[int] = mapped_column(nullable=False, default=1)


    user: Mapped[list["UserProfile"]] = relationship(back_populates='contributions')

    # Set the value of advance_month - (amount/slot)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)