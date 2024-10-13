from typing import Any

from src.domain.models.ticket import Ticket
from src.domain.models.ticket_item import TicketItem
from src.domain.repositories.ticket import TicketRepository
from src.domain.repositories.ticket_item import TicketItemRepository
from src.domain.unit_of_work import UnitOfWork


class LoadTicketsInDBUseCase:
    def __init__(
        self,
        tickets_repository: TicketRepository,
        ticket_items_repository: TicketItemRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.__tickets_repository = tickets_repository
        self.__ticket_items_repository = ticket_items_repository
        self.__unit_of_work = unit_of_work

    def handle(self, ticket_data: dict[str, Any]) -> None:
        with self.__unit_of_work():
            ticket = self.__tickets_repository.create_ticket(
                Ticket(timestamp=ticket_data["timestamp"])
            )
            self.__unit_of_work.flush()
            for item in ticket_data["items"]:
                self.__ticket_items_repository.create_ticket_item(
                    TicketItem(
                        quantity=item["quantity"],
                        description=item["description"],
                        unit_price=item["unit_price"],
                        total_price=item["total_price"],
                        ticket_id=ticket.id,
                        is_weighted_product=float(item["quantity"])
                        != int(item["quantity"]),
                    )
                )
