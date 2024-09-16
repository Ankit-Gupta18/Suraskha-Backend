from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from routers.external.verify_adhaar import verify_adhaar_with_api
from routers.external.otp_service_twilio import send_otp_via_twilio
from routers.utils.otp_store_and_verify import store_otp, verify_otp
import requests
from db.dbmanager import DBManager
db_manager = DBManager().get_instance()
import json
import random

router = APIRouter()

# Request payload model
class SignupRequest(BaseModel):
    name: str
    adhaar_number: str
    phone_number: str
    email: str

# Request payload model for OTP verification
class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

@router.post("/user_signup_generate_otp")
async def user_signup(payload: SignupRequest):

    existing_user = db_manager.get_user_by_phone(payload.phone_number)
    
    if existing_user:
        return {"status": "ok", "message": "User already exists"}  # Return 200 if user already exists

    # Step 1: Verify Aadhaar
    adhaar_response = verify_adhaar_with_api(payload.adhaar_number)

    print(adhaar_response)
    
    if adhaar_response.get("status_code") == 200 or adhaar_response.get("sub_code") == "INVALID_AADHAAR_NUMBER":
        raise HTTPException(status_code=400, detail="Aadhaar verification failed, Invalid adhaar number")
    elif adhaar_response.get("status") == "failed":
        raise HTTPException(status_code=400, detail="Aadhaar verification failed")

    # Step 2: Match last three digits of Aadhaar and phone number
    adhaar_last_three = adhaar_response.get("last_digits")
    phone_number_exists = adhaar_response.get("is_mobile")
    phone_last_three = payload.phone_number[-3:]

    if phone_number_exists and str(adhaar_last_three) != str(phone_last_three):
        raise HTTPException(status_code=400, detail="Phone number and Aadhaar mismatch")

    # Step 3: Generate OTP
    otp = random.randint(100000, 999999)
    store_otp(payload.phone_number, otp)

    # Step 4: Send OTP via Twilio
    send_otp_via_twilio(payload.phone_number, otp)

    #Step 5: Add in DB
    name = payload.name
    phone_number = payload.phone_number
    email = payload.email

    # Extracting data from the API response to form the payload
    payload = {
        "name": name,
        "adhaar_number": adhaar_response["data"]["aadhaar_number"],
        "state": adhaar_response["data"]["state"],
        "age_group": adhaar_response["data"]["age_range"],
        "gender": adhaar_response["data"]["gender"],
        "phone_number": phone_number,
        "email": email
    }

    db_manager.insert_user_auth(payload)

    return {"status": "ok", "message": "OTP sent successfully"}


@router.post("/user_signup_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        db_manager.delete_user_by_phone(payload.phone_number)
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"status": "ok", "message": "OTP verified successfully"}
