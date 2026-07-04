import yagmail
from config import *

def send_email_alert():
    try:
        yag = yagmail.SMTP(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        yag.send(
            EMAIL_RECEIVER,
            "Driver Drowsiness Alert",
            "Driver appears drowsy."
        )

        print("Email Sent")

    except Exception as e:
        print("Email Error:", e)