from abc import ABC, abstractmethod
from typing import Generator


class EmailConnector(ABC):
    @abstractmethod
    def get_emails(self, query: str) -> list:
        pass

    @abstractmethod
    def find_attachments(
        self, email_id: str, filename_contains: str
    ) -> Generator[bytes, None, None]:
        pass

    @abstractmethod
    def mark_as_read(self, email_id: str) -> None:
        pass
