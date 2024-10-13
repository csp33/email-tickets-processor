from abc import abstractmethod, ABC

from src.domain.models.ticket_item import TicketItem


class TicketItemRepository(ABC):
    @abstractmethod
    def create_ticket_item(self, ticket_item: TicketItem) -> TicketItem:
        pass
