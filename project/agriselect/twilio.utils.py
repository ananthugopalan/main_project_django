# twilio_utils.py
from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'AC784edca2d4dc48edab5e0eb39519d949'
    auth_token = 'b4f393289f7f588341d23277806cdaa3'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Your order has been placed!!!Thank you for choosing AgriSelect.',
            to='whatsapp:+917306053696'
        )
        print("Message sent successfully:"  , message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False
    