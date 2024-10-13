from logging import Logger
from typing import Generator

from src.domain.connectors.email import EmailConnector


class GetTicketFilesUseCase:
    def __init__(
        self, email_connector: EmailConnector, sender_emails: list[str], logger: Logger
    ) -> None:
        self.__email_connector = email_connector
        self.__sender_emails = sender_emails
        self.__logger = logger

    def handle(self) -> Generator[tuple[str, bytes], None, None]:
        for email in self.__email_connector.get_emails(self.__get_query()):
            email_id = email["id"]
            self.__logger.info(f"Processing email {email_id}")
            yield email_id, self.__get_first_attachment_content(email_id)

    def __get_query(self) -> str:
        filters = [
            " OR ".join([f"from:{sender}" for sender in self.__sender_emails]),
            "is:unread",
            "has:attachment",
        ]
        return " ".join(filters)

    def __get_first_attachment_content(self, email_id: str) -> bytes:
        return list(
            self.__email_connector.find_attachments(
                email_id=email_id, filename_contains="pdf"
            )
        )[0]
