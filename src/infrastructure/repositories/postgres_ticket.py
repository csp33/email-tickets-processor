from sqlalchemy.orm import Session

from src.domain.models.ticket import Ticket
from src.domain.repositories.ticket import TicketRepository


class PostgresTicketRepository(TicketRepository):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create_ticket(self, ticket: Ticket) -> Ticket:
        self.__session.add(ticket)
        return ticket
