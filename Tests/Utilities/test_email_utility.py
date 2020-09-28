#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test email related utility function."""


import smtplib
import ssl

from credentials import email
from credentials import password


def test_send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email
    receiver_email = email
    # password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
