import smtplib, ssl

port = 465  # For SSL
password = input("Type your password and press enter: ")

sender_email = "my@gmail.com"
receiver_email = "your@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

# Send email here

# Create a secure SSL context
context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("awannaphasch2016@gmail.com", password)
#     # TODO: Send email here