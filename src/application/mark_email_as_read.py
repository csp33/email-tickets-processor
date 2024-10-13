from logging import Logger

from src.domain.connectors.email import EmailConnector


class MarkEmailAsReadUseCase:
    def __init__(self, email_connector: EmailConnector, logger: Logger) -> None:
        self.__email_connector = email_connector
        self.__logger = logger

    def handle(self, email_id: str) -> None:
        self.__logger.info(f"Marking email {email_id} as read")
        self.__email_connector.mark_as_read(email_id=email_id)
