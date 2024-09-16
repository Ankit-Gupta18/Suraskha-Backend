from twilio.rest import Client
import os

# Fetch credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

# Function to send OTP via Twilio
def send_otp_via_twilio(phone_number: str, otp: str):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=twilio_phone_number,
        to=f"{phone_number}"
    )

    print(f"Message sent with OTP!")
