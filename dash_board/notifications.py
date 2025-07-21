from twilio.rest import Client
from django.conf import settings

def send_driver_link(driver_phone, fuelreq_id):
    # Replace with actual domain
    link = f"https://sllhub.com/signature/{fuelreq_id}/"
    message_body = (
        f"Hi, please confirm your fuel request:\n{link}"
    )

    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

    # Make sure driver_phone is formatted as '+15551234567' (international format)
    client.messages.create(
        body=message_body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,   # 'whatsapp:+14155238886' from your .env
        to=f"whatsapp:{driver_phone}"
    )
