#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test email related utility function."""

from credentials import email
from src.Utilities.Emails.email_utility import send_email


def test_send_email():
    # password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    send_email(message, email)
