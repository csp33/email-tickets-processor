import os
import tempfile
from typing import Any

import requests


class TransformPDFToJSONUseCase:
    def __init__(self, api_url: str) -> None:
        self.__api_url = api_url

    def handle(self, file_content: bytes) -> dict[str, Any]:
        with tempfile.NamedTemporaryFile(
            delete=False
        ) as temp_file:  # TODO this logic should be encapsulated in a class
            temp_file.write(file_content)
            temp_file.flush()

            return self.__send_pdf_to_api(temp_file.name)

    def __send_pdf_to_api(self, tmp_filename: str) -> dict[str, Any]:
        with open(tmp_filename, "rb") as f:
            files = {
                "ticket_file": (os.path.basename(tmp_filename), f, "application/pdf")
            }
            response = requests.post(
                self.__api_url, files=files
            )  # TODO move to a connector
            response.raise_for_status()
            return response.json()
