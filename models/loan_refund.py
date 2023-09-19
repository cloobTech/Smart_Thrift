#!/usr/bin/python3
"""Module for loan refunded"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanRefund(BaseModel, Base):
    """class - (table) represents refunded"""
    __tablename__ = "loan_refunds"
    date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    guarantor_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)
    loan_id: Mapped[str] = mapped_column(
        ForeignKey('loan.id'), nullable=False)
    # loan_profile_id: Mapped[str] = mapped_column(
    #     ForeignKey('loan_profile.id'), nullable=False)

    # loan_profile: Mapped["LoanProfile"] = relationship(
    #     back_populates="loan_refund")
    user: Mapped["UserProfile"] = relationship(back_populates="loan_refund")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
