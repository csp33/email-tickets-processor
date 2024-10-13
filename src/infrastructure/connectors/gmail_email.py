import base64
from typing import Generator

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.domain.connectors.email import EmailConnector


class GmailEmailConnector(EmailConnector):
    __SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    def __init__(self, token_filepath: str) -> None:
        credentials = Credentials.from_authorized_user_file(
            token_filepath, self.__SCOPES
        )
        self.__service = build("gmail", "v1", credentials=credentials)

    def get_emails(self, query: str) -> list:
        results = (
            self.__service.users()
            .messages()
            .list(userId="me", q=query, labelIds=["INBOX"], maxResults=10)
            .execute()
        )
        return results.get("messages", [])

    def find_attachments(
        self, email_id: str, filename_contains: str
    ) -> Generator[bytes, None, None]:
        email = (
            self.__service.users().messages().get(userId="me", id=email_id).execute()
        )
        for part in email["payload"]["parts"]:
            if part["filename"] and filename_contains in part["filename"]:
                attachment_id = part["body"]["attachmentId"]
                attachment = self.__get_attachment(
                    email_id=email_id, attachment_id=attachment_id
                )

                yield base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))

    def __get_attachment(self, email_id: str, attachment_id: str) -> dict:
        return (
            self.__service.users()
            .messages()
            .attachments()
            .get(userId="me", messageId=email_id, id=attachment_id)
            .execute()
        )

    def mark_as_read(self, email_id: str) -> None:
        self.__service.users().messages().modify(
            userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}
        ).execute()
