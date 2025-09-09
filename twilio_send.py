from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def send_whatsapp_message(to, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=f"whatsapp:{to}"
    )
    return message.sid