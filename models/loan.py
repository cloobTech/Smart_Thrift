#!/usr/bin/python3
"""Module for loan given out"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Loan(BaseModel, Base):
    """class - (table) represents loan given out"""
    __tablename__ = "loan"
    is_member: Mapped[bool] = mapped_column(nullable=False, default=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    guarantor_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)

    # Relationship
    user: Mapped["UserProfile"] = relationship(back_populates="loan")
    loan_profile: Mapped["LoanProfile"] = relationship(
        back_populates="loan")
    interest: Mapped["Interest"] = relationship(
        back_populates="loan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
