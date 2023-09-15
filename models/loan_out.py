#!/usr/bin/python3
"""Module for loan given out"""
from datetime import datetime, timedelta
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoanOut(BaseModel, Base):
    """class - (table) represents loan given out"""
    __tablename__ = "loan_out"
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    guarantor: Mapped[str] = mapped_column(String(60), nullable=True)
    guarantor_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False, default=lambda context: 
    context.get_current_parameters()['start_date'] + timedelta(days=30))
    loan_status: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_member: Mapped[bool] = mapped_column(nullable=False, default=False)
    interest: Mapped[float] = mapped_column(nullable=False, default=0)
    total: Mapped[float] = mapped_column(nullable=False)

    member: Mapped["User"] = relationship(back_populates="loan_out")

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__calculate_interest(kwargs)    
            self.__loan_total(kwargs)
        super().__init__(*args, **kwargs)

    def __calculate_interest(self, dict_attr: dict) -> None:
        """Calculate the interest of a debtor"""
        rate = 0.10 #interest rate on loan
        member_status = dict_attr.get('is_member', None) #check if user is a member
        amount = dict_attr.get('amount', None) #principal
        if member_status:
            rate = 0.05
        interest = amount * rate
        dict_attr['interest'] = interest
        for key, value in dict_attr.items():
            setattr(self, key, value)

    def __loan_total(self, dict_attr: dict):
        """Total expected cash (Principal + Interest)"""
        amount = dict_attr.get('amount', None)
        interest = dict_attr.get('interest', None)
        total = amount + interest
        setattr(self, 'total', total)