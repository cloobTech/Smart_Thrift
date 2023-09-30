#!/usr/bin/python3
"""Module for interest on loan given out"""
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Interest(BaseModel, Base):
    """class - (table) represents interest on loan given out"""
    __tablename__ = "interest"
    amount: Mapped[float] = mapped_column(nullable=False)
    refund_id: Mapped[str] = mapped_column(
        ForeignKey('loan_refunds.id'), nullable=False)
    guarantor_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)

    # Relationship
    refund: Mapped["LoanRefund"] = relationship(back_populates="interest")
    user: Mapped["UserProfile"] = relationship(back_populates="interest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
