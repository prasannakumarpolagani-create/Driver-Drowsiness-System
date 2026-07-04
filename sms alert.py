from twilio.rest import Client
from config import *

def send_sms_alert():
    try:
        client = Client(
            TWILIO_SID,
            TWILIO_TOKEN
        )

        client.messages.create(
            body="Driver Drowsiness Alert!",
            from_=TWILIO_PHONE,
            to=RECEIVER_PHONE
        )

        print("SMS Sent")

    except Exception as e:
        print("SMS Error:", e)