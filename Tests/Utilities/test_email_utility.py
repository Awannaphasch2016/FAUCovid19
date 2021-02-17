#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test email related utility function."""
import pytest

from credentials import EMAIL
from src.Utilities.Emails.email_utility import send_email


@pytest.mark.test_utility_function
def test_send_email():
    # password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    send_email(message, EMAIL)
