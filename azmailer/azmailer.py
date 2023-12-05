
import os
from azure.communication.email import EmailClient
from azure.core.exceptions import AzureError
import base64
from typing import Union
from pathutility.pathutils import PathUtils as pu
# get_filename,get_dir_extension
import mimetypes

class AzMailer:
    """Class for sending emails with Azure Communication Services.

    Inspired by the documentation:
    https://learn.microsoft.com/en-us/azure/communication-services/quickstarts/email/send-email?tabs=linux%2Cconnection-string&pivots=programming-language-python

    :Usage:
    
    .. code-block:: python
    
        from azmailer import AzMailer
        mailer = AzMailer(os.environ["AZURE_COMMUNICATION_CONNECTION_STRING"], os.environ["AZURE_COMMUNICATION_SENDER_ADDRESS"])
        email_message = mailer.construct_message(
            subject="Attached code",
            content="<html><body><h1>A code!</h1>to control them all!</body></html>",
            # content="a code to control them all!",
            to_addresses=["marcanglisano@gmail.com"],
            attachments=["path/to/file1","path/to/file2"]
        )
        mailer.send_email(email_message)
        
    """
    
    POLLER_WAIT_TIME=10 # utilitzar el decordor de timeout k vaig fer
    def __init__(self, connection_string: str, sender_address: str):
        """Initialize the AzMailer.

        Args:
            connection_string (str): Azure Communication Service connection string.
            sender_address (str): Email address of the sender.
        """
        self.connection_string = connection_string
        self.sender_address = sender_address
        self.email_client = EmailClient.from_connection_string(
            self.connection_string)

    def send_email(self, message: dict):
        """Send an email.

        Args:
            message (dict): Email message dictionary.

        Raises:
            RuntimeError: If sending the email fails.
        """
        try:
            poller = self.email_client.begin_send(message)

            time_elapsed = 0
            while not poller.done():
                print("Email send poller status: " + poller.status())

                poller.wait(self.POLLER_WAIT_TIME)
                time_elapsed += self.POLLER_WAIT_TIME

                if time_elapsed > 18 * self.POLLER_WAIT_TIME:
                    raise RuntimeError("Polling timed out.")

            if poller.result()["status"] == "Succeeded":
                print(f"Successfully sent the email (operation id: {poller.result()['id']})")
            else:
                raise RuntimeError(str(poller.result()["error"]))

        except AzureError as azure_error:
            print(f"AzureError occurred: {azure_error}")
            return None

        except Exception as ex:
            print(f"An error occurred: {ex}")
            return None

    def construct_message(self, 
        subject: str, 
        content: str,
        to_addresses: list, 
        cc_addresses: list = None, 
        bcc_addresses: list = None,
        
        attachments: Union[list, str] = None,
        user_engagement_tracking_disabled: bool = False,
    )->dict:
        """Construct an email message.

        Args:
            subject (str): Email subject.
            content (str): Email content (HTML or plain text).
            to_addresses (list): List of recipient email addresses.
            cc_addresses (list, optional): List of CC email addresses. Defaults to None.
            bcc_addresses (list, optional): List of BCC email addresses. Defaults to None.
            attachments (Union[list, str], optional): List of file paths or a single file path to attach. Defaults to None.
            user_engagement_tracking_disabled (bool, optional): Disable user engagement tracking. Defaults to False.

        Returns:
            dict: Constructed email message dictionary.
        """
        bcc_addresses = [{"address": address} for address in bcc_addresses] if bcc_addresses else []
        cc_addresses = [{"address": address} for address in cc_addresses] if cc_addresses else []
        message = {
            "content": {
                "subject": subject,
            },
            "recipients": {
                "to": [{"address": address} for address in to_addresses],
                "bcc": bcc_addresses,
                "cc": cc_addresses
            },
            "senderAddress": self.sender_address,
            "attachments": [],
            "userEngagementTrackingDisabled": user_engagement_tracking_disabled

        }

        # Add content based on whether it's HTML or plain text
        if content:
            message["content"]["html" if "<html>" in content else "plainText"] = content

        # Process attachments
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]

            for attachment_path in attachments:
                with open(attachment_path, "rb") as file:
                    file_content = file.read()

                attachment_content = base64.b64encode(file_content).decode("utf-8")
                attachment_name = pu.get_filename(attachment_path)+pu.get_file_extension(attachment_path)
                mime_type, _ = mimetypes.guess_type(attachment_path)
                message["attachments"].append({
                    "contentInBase64": attachment_content,
                    "contentType": mime_type,  # Set the content type accordingly
                    "name": attachment_name
                })

        return message

if __name__ == "__main__":
    mailer = AzMailer(os.environ["AZURE_COMMUNICATION_CONNECTION_STRING"], os.environ["AZURE_COMMUNICATION_SENDER_ADDRESS"])
    email_message1 = mailer.construct_message(
        subject="adjuto este mismo codigo",
        content="<html><body><h1>un codigo!</h1>para controlarlos a todos!</body></html>",
        # content="""
        # hola 
        # tonto
        # """,
        to_addresses=["manglisano@servihabitat.com"]

        # attachments=[r"C:\Users\u2y20946\OneDrive - SERVIHABITAT SERVICIOS INMOBILIARIOS, S.L\Documents\GitHub\svh_azure-1\test_mail.py"]
    )

        # content="""hola
        # niga"""

    mailer.send_email(email_message1)
