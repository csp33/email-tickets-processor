from abc import ABC, abstractmethod
from typing import Any


class TicketsAnalyzerAPIConnector(ABC):
    def __init__(self, api_url: str) -> None:
        self._api_url = api_url

    @abstractmethod
    def send_pdf(self, filepath: str, supermarket_name: str) -> dict[str, Any]:
        pass
