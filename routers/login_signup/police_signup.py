from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from routers.external.verify_adhaar import verify_adhaar_with_api
from routers.external.otp_service_twilio import send_otp_via_twilio
from routers.utils.otp_store_and_verify import store_otp, verify_otp
from routers.utils.smtp_client import SMTPClient
import random
import base64
from db.dbmanager import DBManager
db_manager = DBManager().get_instance()

# Temporary store for signup details until OTP verification
signup_temp_store = {}

router = APIRouter()
smtp_client = SMTPClient()

# Request payload model
class SignupRequest(BaseModel):
    name: str
    police_id: str
    police_station_address: str
    phone_number: str
    email: str
    id_card: bytearray

# Request payload model for OTP verification
class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

@router.post("/police_signup_generate_otp")
async def user_signup(payload: SignupRequest):

    existing_user = db_manager.get_police_by_phone(payload.phone_number)
    
    if existing_user:
        return {"status": "ok", "message": "Police user already exists"}  # Return 200 if user already exists

    # Step 1: Generate OTP
    otp = random.randint(100000, 999999)
    store_otp(payload.phone_number, otp)

    # Step 2: Send OTP via Twilio
    send_otp_via_twilio(payload.phone_number, otp)

    # Step 3: Store the police user's details temporarily until OTP verification
    signup_temp_store[payload.phone_number] = {
        "name": payload.name,
        "police_id": payload.police_id,
        "police_station_address": payload.police_station_address,
        "phone_number": payload.phone_number,
        "email": payload.email,
        "id_card": payload.id_card
    }

    return {"status": "ok", "message": "OTP sent successfully"}


@router.post("/police_signup_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        if payload.phone_number in signup_temp_store:
            del signup_temp_store[payload.phone_number]  # Remove temp data on failure
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Step 2: Fetch Aadhaar details and user details from the temporary store
    if payload.phone_number not in signup_temp_store:
        raise HTTPException(status_code=400, detail="No signup data found for this phone number")

    user_details = signup_temp_store[payload.phone_number]
    del signup_temp_store[payload.phone_number]  # Remove after verification

    # Step 3: Add user data to DB
    db_payload = {
        "name": user_details["name"],
        "police_id": user_details["police_id"],
        "police_station_address": user_details["police_station_address"],
        "phone_number": user_details["phone_number"],
        "email": user_details["email"],
        "id_card": user_details["id_card"],  # This will be the bytea data
    }

    db_manager.insert_police_auth(db_payload)

    # Step 4: Send verification email to admin
    admin_email = "admin@example.com"  # Admin email where police signups are sent
    subject_admin = "Police Signup Verification"
    message_admin = f"""
    Hi Admin,

    A new user has signed up as police, please verify the details below:

    Name: {user_details['name']}
    Police ID: {user_details['police_id']}
    Police Station Address: {user_details['police_station_address']}
    Phone Number: {user_details['phone_number']}
    Email: {user_details['email']}

    Attached is the ID card image for verification.

    Best regards,
    Suraksha Backend Team
    """

    # Attach ID card for admin email
    id_card_image = user_details["id_card"]

    # Send admin email with the ID card attachment
    smtp_client.send_verification_mail(admin_email, subject_admin, message_admin, id_card_image)

    # Step 5: Send confirmation email to user
    user_email = user_details["email"]  # User's email
    subject_user = "Signup Request Received"
    message_user = f"""
    Hi {user_details['name']},

    Your signup request has been received for verification with the following details:

    Name: {user_details['name']}
    Police ID: {user_details['police_id']}
    Police Station Address: {user_details['police_station_address']}
    Phone Number: {user_details['phone_number']}
    Email: {user_details['email']}

    We will get back to you once the verification is complete.

    Best regards,
    Suraksha Backend Team
    """

    # Send email to the user without the ID card attachment
    smtp_client.send_verification_mail(user_email, subject_user, message_user, id_card_image)

    return {"status": "ok", "message": "OTP verified, user added successfully, emails sent to admin and user"}
