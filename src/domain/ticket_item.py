from sqlalchemy import Column, Float, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.domain.base import Base


class TicketItem(Base):
    __tablename__ = "ticket_items"

    id = Column(Integer, primary_key=True)
    quantity = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    is_weighted_product = Column(Boolean, nullable=False)

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    ticket = relationship("Ticket", back_populates="items")
