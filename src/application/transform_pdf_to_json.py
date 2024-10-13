from typing import Any


from src.domain.connectors.tickets_analyzer_api import TicketsAnalyzerAPIConnector
from src.domain.tmp_file_manager import TmpFileManager


class TransformPDFToJSONUseCase:
    def __init__(
        self,
        api_connector: TicketsAnalyzerAPIConnector,
        supermarket_name: str,
        tmp_file_manager: TmpFileManager,
    ) -> None:
        self.__api_connector = api_connector
        self.__supermarket_name = supermarket_name
        self.__tmp_file_manager = tmp_file_manager

    def handle(self, file_content: bytes) -> dict[str, Any]:
        with self.__tmp_file_manager(file_content) as tmp_filename:
            return self.__api_connector.send_pdf(
                filepath=tmp_filename, supermarket_name=self.__supermarket_name
            )
