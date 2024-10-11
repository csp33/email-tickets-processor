from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TicketItem(Base):
    __tablename__ = "ticket_items"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    description = Column(String)
    unit_price = Column(Float)
    total_price = Column(Float)
