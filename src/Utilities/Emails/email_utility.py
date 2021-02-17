#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contain email related utility function."""

import smtplib
import ssl

from credentials import EMAIL
from credentials import EMAIL_PASSWORD
from src.Utilities.Logging import MyLogger

LOGGER = MyLogger()
PROGRAM_LOGGER = LOGGER.program_logger

def send_email(message: str, receiver_email: str) -> None:
    """Send message to email.



    Note: both receiver_email and sender_email must use gmail. This is because
        different email services required different security protocol standard

    :param message: message to be sent
    :param receiver_email: email of a person that message will be sent to
    """
    PROGRAM_LOGGER.info(f"Sending email to {receiver_email}")
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = EMAIL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, EMAIL_PASSWORD)
        server.sendmail(sender_email, receiver_email, message)
