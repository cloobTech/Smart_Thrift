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
    
    member_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    contribution_date: Mapped[datetime] = mapped_column(nullable=False)
    advance_month: Mapped[int] = mapped_column(nullable=True, default=0)

    member: Mapped[list["User"]] = relationship(back_populates='contribution')

    # Set the value of advance_month - (amount/slot)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)