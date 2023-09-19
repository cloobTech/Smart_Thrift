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
    loan_status: Mapped[bool] = mapped_column(nullable=False, default=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users_profile.id'), nullable=False)
    loan_id: Mapped[str] = mapped_column(
        ForeignKey('loan.id'), nullable=False)
    interest: Mapped[float] = mapped_column(nullable=False, default=0)
    total: Mapped[float] = mapped_column(nullable=False)

    # Relationships
    user: Mapped["UserProfile"] = relationship(back_populates="loan_profile")
    loan: Mapped["Loan"] = relationship(back_populates="loan_profile")
    # loan_refund: Mapped["LoanRefund"] = relationship(
    #     back_populates="loan_profile")

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__calculate_interest(kwargs)
            self.__loan_total(kwargs)
        super().__init__(*args, **kwargs)

    def __calculate_interest(self, dict_attr: dict) -> None:
        """Calculate the interest of a debtor"""
        rate = 0.10  # interest rate on loan
        # check if user is a member
        member_status = dict_attr.get('is_member', None)
        principal = dict_attr.get('principal', None)  # principal
        if member_status:
            rate = 0.05
        interest = principal * rate
        dict_attr['interest'] = interest
        for key, value in dict_attr.items():
            setattr(self, key, value)

    def __loan_total(self, dict_attr: dict):
        """Total expected cash (Principal + Interest)"""
        principal = dict_attr.get('principal', None)
        interest = dict_attr.get('interest', None)
        total = principal + interest
        setattr(self, 'total', total)
