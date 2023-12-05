# AzMailer

## Introduction
AzMailer is a Python class designed to facilitate sending emails using Azure Communication Services.

Inspired by the Azure Communication Services documentation [here](https://learn.microsoft.com/en-us/azure/communication-services/quickstarts/email/send-email?tabs=linux%2Cconnection-string&pivots=programming-language-python), AzMailer simplifies the process of sending emails by providing an easy-to-use interface for constructing and sending email messages.


## Installation
To install azmailer, simply use pip:

```bash
pip install azmailer

```

## Usage Example
To use the AzMailer class, follow these steps:

1. Initialize the AzMailer object with the Azure Communication Service connection string and sender's email address:

    ```python
    mailer = AzMailer(AZURE_CONNECTION_STRING, SENDER_EMAIL_ADDRESS)
    ```

2. Construct an email message using the `construct_message()` method:

    ```python
    email_message = mailer.construct_message(
        subject="Your Email Subject",
        content="Your Email Content",
        to_addresses=["recipient1@example.com", "recipient2@example.com"],
        attachments=["/path/to/file1", "/path/to/file2"]
    )
    ```

3. Send the email message using the `send_email()` method:

    ```python
    mailer.send_email(email_message)
    ```


## Documentation
The Sphinx-generated documentation for azmailer can be found [here](https://anglisanosa.github.io/azmailer/).

## Contribution
Feel free to contribute by submitting issues [here](https://github.com/anglisanosa/azmailer/issues).