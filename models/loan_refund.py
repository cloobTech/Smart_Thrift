#!/usr/bin/python3
"""Module for loan refunded"""
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanRefund(BaseModel, Base):
    """class - (table) represents refunded"""
    __tablename__ = "loan_refunds"
    amount: Mapped[float] = mapped_column(nullable=False)
    loan_id: Mapped[str] = mapped_column(
        ForeignKey('loan.id'), nullable=False)

    interest: Mapped["Interest"] = relationship(
        back_populates="refund", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
