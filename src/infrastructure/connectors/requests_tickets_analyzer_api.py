from typing import Any

import requests

from src.domain.connectors.tickets_analyzer_api import TicketsAnalyzerAPIConnector


class RequestsTicketsAnalyzerApiConnector(TicketsAnalyzerAPIConnector):
    def send_pdf(self, filepath: str, supermarket_name: str) -> dict[str, Any]:
        with open(filepath, "rb") as f:
            files = {"ticket_file": (filepath, f, "application/pdf")}
            response = requests.post(self.__get_url(supermarket_name), files=files)
            response.raise_for_status()
            return response.json()

    def __get_url(self, supermarket_name: str) -> str:
        return f"{self._api_url}/{supermarket_name}"
