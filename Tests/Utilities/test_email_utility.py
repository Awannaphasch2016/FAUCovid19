#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test email related utility function."""


import smtplib
import ssl


def test_send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "terngoodod@gmail.com"  # Enter your address
    receiver_email = "terngoodod@gmail.com"  # Enter receiver address
    # password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    # password = 'Terng2258'
    with open(password)
    # password = 'Yeeha1234'
    #
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
