from sqlalchemy import Integer, Column, DateTime
from sqlalchemy.orm import relationship

from src.domain.models.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, unique=True)
    items = relationship("TicketItem", back_populates="ticket")
