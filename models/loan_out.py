#!/usr/bin/python3
"""Module for loan given out"""
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanOut(BaseModel, Base):
    """Represents each loan instance given out"""
    __tablename__ = "loan_out"
    loan_id: Mapped[str] = mapped_column(ForeignKey('loan.id'), nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            # format for datetime
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            if "start_date" in kwargs and type(kwargs["start_date"]) is str:
                kwargs['start_date'] = datetime.strptime(
                    kwargs["start_date"], time_format)
            if "end_date" in kwargs and type(kwargs["end_date"]) is str:
                kwargs['end_date'] = datetime.strptime(
                    kwargs["end_date"], time_format)
        super().__init__(*args, **kwargs)
