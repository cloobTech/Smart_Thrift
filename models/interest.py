#!/usr/bin/python3
"""Module for interest on loan given out"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Interest(BaseModel, Base):
    """class - (table) represents interest on loan given out"""
    __tablename__ = "interest"
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    loan_id: Mapped[str] = mapped_column(
        ForeignKey('loan.id'), nullable=False)
    guarantor_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)

    # Relationship
    loan: Mapped["Loan"] = relationship(back_populates="interest")
    user: Mapped["UserProfile"] = relationship(back_populates="interest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
