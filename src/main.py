import base64
import os
import tempfile

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.base import Base
from src.domain.ticket import Ticket
from src.domain.ticket_item import TicketItem

API_URL = os.environ["API_URL"]
SENDER_EMAILS = os.environ["ALLOWED_EMAILS"].split(",")
DATABASE_URL = os.environ["DATABASE_URL"]

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


def authenticate_gmail():
    return Credentials.from_authorized_user_file("/files/token.json", SCOPES)


def check_for_new_emails(service):
    query = f"({' OR '.join([f'from:{sender}' for sender in SENDER_EMAILS])}) is:unread has:attachment"
    results = (
        service.users()
        .messages()
        .list(userId="me", q=query, labelIds=["INBOX"], maxResults=10)
        .execute()
    )
    messages = results.get("messages", [])

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        process_email(msg, service, message["id"])


def process_email(msg, service, message_id):
    for part in msg["payload"]["parts"]:
        if part["filename"] and "pdf" in part["filename"]:
            attachment_id = part["body"]["attachmentId"]
            attachment = (
                service.users()
                .messages()
                .attachments()
                .get(userId="me", messageId=msg["id"], id=attachment_id)
                .execute()
            )
            file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_data)
                temp_file.flush()

                send_pdf_to_api(temp_file.name)

            mark_as_read(service, message_id)


def send_pdf_to_api(temp_filename):
    with open(temp_filename, "rb") as f:
        files = {"ticket_file": (os.path.basename(temp_filename), f, "application/pdf")}
        response = requests.post(API_URL, files=files)
        response.raise_for_status()
        ingest_data_to_postgres(response.json())


def ingest_data_to_postgres(data):
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_ticket = Ticket(timestamp=data["timestamp"])
    session.add(new_ticket)
    session.commit()

    for item in data["items"]:
        new_item = TicketItem(
            quantity=item["quantity"],
            description=item["description"],
            unit_price=item["unit_price"],
            total_price=item["total_price"],
            ticket_id=new_ticket.id,
        )
        session.add(new_item)

    session.commit()
    session.close()


def mark_as_read(service, message_id):
    service.users().messages().modify(
        userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def main():
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    check_for_new_emails(service)


if __name__ == "__main__":
    main()
