#!/usr/bin/python3
""" User's Profile Model  """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AdminLog(BaseModel, Base):
    """Admin log class"""
    __tablename__ = 'admin_logs'

    admin_id: Mapped[str] = mapped_column(
        String(60), ForeignKey('users_profile.id'), nullable=False)
    entity_id: Mapped[str] = mapped_column(nullable=False)
    operation: Mapped[str] = mapped_column(nullable=False)
    details: Mapped[str] = mapped_column(nullable=False)
