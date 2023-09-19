#!/usr/bin/python3
""" User's Profile Model  """
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class UserProfile(BaseModel, Base):
    """User's Profile Class (Table)"""
    __tablename__ = "users_profile"
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates='user_profile', uselist=False)
    contributions: Mapped[List["Contribution"]] = relationship(
        back_populates='user')
    loan: Mapped[List["Loan"]] = relationship(
        back_populates='user')
    loan_profile: Mapped[List["LoanProfile"]] = relationship(
        back_populates='user')
    loan_refund: Mapped[List["LoanRefund"]] = relationship(
        back_populates='user')
    interest: Mapped[List["Interest"]] = relationship(
        back_populates='user')
