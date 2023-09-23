#!/usr/bin/python3
""" User's Profile Model  """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class UserProfile(BaseModel, Base):
    """User's Profile Class (Table)"""
    __tablename__ = "users_profile"

    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[str] = mapped_column(
        String(60), nullable=False, default='member')
    slot: Mapped[int] = mapped_column(nullable=False, default=1)
    registered: Mapped[bool] = mapped_column(nullable=False, default=True)
    month_covered: Mapped[int] = mapped_column(nullable=False, default=0)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates='user_profile', uselist=False)
    contributions: Mapped[List["Contribution"]] = relationship(
        cascade='all, delete-orphan')
    loan: Mapped[List["Loan"]] = relationship(cascade='all, delete-orphan')
    loan_profile: Mapped[List["LoanProfile"]] = relationship(
        back_populates='user')
    loan_refund: Mapped[List["LoanRefund"]] = relationship(
        back_populates='user')
    interest: Mapped[List["Interest"]] = relationship(
        back_populates='user')
