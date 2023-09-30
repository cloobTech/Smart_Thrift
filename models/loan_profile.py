#!/usr/bin/python3
"""Module for loan given out"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanProfile(BaseModel, Base):
    """class - (table) represents profile loan given out"""
    __tablename__ = "loan_profile"
    principal: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False, default=False)
    loan_id: Mapped[str] = mapped_column(
        ForeignKey('loan.id'), nullable=False)
    interest: Mapped[float] = mapped_column(nullable=False, default=0)
    total: Mapped[float] = mapped_column(nullable=False)

    # Relationship
    loan: Mapped['Loan'] = relationship(back_populates='loan_profile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
