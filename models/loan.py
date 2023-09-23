#!/usr/bin/python3
"""Module for loan related activities"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Loan(BaseModel, Base):
    """
    class - (table) represents agrregate loan given out and links to other
    loan related activities like refund, interest, etc
    """
    __tablename__ = "loan"
    is_member: Mapped[bool] = mapped_column(nullable=False, default=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False, default=0)
    guarantor_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)
    
    # Relationship
    loan_out: Mapped[List['LoanOut']] = relationship(cascade="all, delete-orphan")
    loan_profile: Mapped["LoanProfile"] = relationship(
        back_populates="loan")
    interest: Mapped["Interest"] = relationship(
        back_populates="loan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
