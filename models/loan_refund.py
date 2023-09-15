#!/usr/bin/python3
"""Module for loan refunded"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanRefund(BaseModel, Base):
    """class - (table) represents refunded"""
    __tablename__ = "loan_refunds"
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    guarantor: Mapped[str | None] = mapped_column(String(60), nullable=True)
    loanout_id: Mapped[str] = mapped_column(ForeignKey('loan_out.id'), nullable=False)
    member_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)

    member: Mapped["User"] = relationship(back_populates="loan_out")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
