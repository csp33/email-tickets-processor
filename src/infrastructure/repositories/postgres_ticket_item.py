from sqlalchemy.orm import Session

from src.domain.models.ticket_item import TicketItem
from src.domain.repositories.ticket_item import TicketItemRepository


class PostgresTicketItemRepository(TicketItemRepository):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create_ticket_item(self, ticket_item: TicketItem) -> TicketItem:
        self.__session.add(ticket_item)
        return ticket_item
