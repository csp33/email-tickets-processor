import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.application.get_ticket_files import GetTicketFilesUseCase
from src.application.load_tickets_in_db import LoadTicketsInDBUseCase
from src.application.mark_email_as_read import MarkEmailAsReadUseCase
from src.application.transform_pdf_to_json import TransformPDFToJSONUseCase
from src.domain.tmp_file_manager import TmpFileManager
from src.infrastructure.connectors.gmail_email import GmailEmailConnector
from src.infrastructure.connectors.requests_tickets_analyzer_api import (
    RequestsTicketsAnalyzerApiConnector,
)
from src.infrastructure.repositories.postgres_ticket import PostgresTicketRepository
from src.infrastructure.repositories.postgres_ticket_item import (
    PostgresTicketItemRepository,
)
from src.infrastructure.sqlalchemy_unit_of_work import SQLAlchemyUnitOfWork

API_URL = os.environ["API_URL"]
SENDER_EMAILS = os.environ["ALLOWED_EMAILS"].split(",")
DATABASE_URL = os.environ["DATABASE_URL"]
TOKEN_FILEPATH = os.environ["TOKEN_FILEPATH"]
SUPERMARKET_NAME = os.environ["SUPERMARKET_NAME"]


def create_session() -> Session:
    engine = create_engine(DATABASE_URL)
    return sessionmaker(bind=engine)()


def create_logger() -> logging.Logger:
    log = logging.getLogger("email-tickets-processor")
    log.setLevel(logging.INFO)
    if not log.hasHandlers():
        stream_handler = logging.StreamHandler(sys.stdout)
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(log_formatter)
        log.addHandler(stream_handler)
    return log


session = create_session()
logger = create_logger()

tmp_file_manager = TmpFileManager()

gmail_email_connector = GmailEmailConnector(token_filepath=TOKEN_FILEPATH)

get_files = GetTicketFilesUseCase(
    email_connector=gmail_email_connector,
    sender_emails=SENDER_EMAILS,
    logger=logger,
)

mark_as_read = MarkEmailAsReadUseCase(
    email_connector=gmail_email_connector,
    logger=logger,
)

transform = TransformPDFToJSONUseCase(
    api_connector=RequestsTicketsAnalyzerApiConnector(API_URL),
    supermarket_name=SUPERMARKET_NAME,
    tmp_file_manager=tmp_file_manager,
)

load = LoadTicketsInDBUseCase(
    tickets_repository=PostgresTicketRepository(session),
    ticket_items_repository=PostgresTicketItemRepository(session),
    unit_of_work=SQLAlchemyUnitOfWork(session),
)

if __name__ == "__main__":
    failed = 0
    success = 0
    for email_id, pdf_content in get_files.handle():
        try:
            email_json = transform.handle(pdf_content)
            load.handle(email_json)
            mark_as_read.handle(email_id)
            success += 1
        except Exception:
            logger.exception("Unable to process email")
            failed += 1
            continue

    logger.info(f"Successfully processed {success} emails")

    if failed > 0:
        raise Exception(f"{failed} emails failed to process")
