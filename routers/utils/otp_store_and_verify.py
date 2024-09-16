from datetime import datetime, timedelta

# In-memory store for OTPs with expiry (for demo purposes)
otp_store = {}

# Store OTP with a timestamp (TTL of 5 minutes)
def store_otp(phone_number: str, otp: str):
    expiry_time = datetime.now() + timedelta(minutes=5)
    otp_store[phone_number] = {"otp": otp, "expires_at": expiry_time}

# Verify OTP and check expiration
from datetime import datetime

def verify_otp(phone_number: str, otp: str) -> bool:

    # Check if phone number is in otp_store
    if phone_number not in otp_store:
        print(f"Phone number {phone_number} not found in OTP store.")
        return False
    
    otp_data = otp_store[phone_number]

    # Check if the OTP is expired
    if datetime.now() > otp_data["expires_at"]:
        print(f"OTP for phone number {phone_number} has expired.")
        del otp_store[phone_number]
        return False
    
    # Check if OTP matches
    if str(otp_data["otp"]) == str(otp):
        print(f"OTP for phone number {phone_number} is correct.")
        del otp_store[phone_number]  # OTP can only be used once
        return True
    
    print(f"OTP for phone number {phone_number} is incorrect.")
    return False

