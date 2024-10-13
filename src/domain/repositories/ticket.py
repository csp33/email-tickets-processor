from abc import abstractmethod, ABC

from src.domain.models.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def create_ticket(self, ticket: Ticket) -> Ticket:
        pass
