from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from routers.external.verify_adhaar import verify_adhaar_with_api
from routers.external.otp_service_twilio import send_otp_via_twilio
from routers.utils.otp_store_and_verify import store_otp, verify_otp
import requests
from db.dbmanager import DBManager
import json
import random

router = APIRouter()

# Request payload model
class SignupRequest(BaseModel):
    adhaar_number: str
    phone_number: str
    email: str

# Request payload model for OTP verification
class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

@router.post("/user_signup_generate_otp")
async def user_signup(payload: SignupRequest):
    # Step 1: Verify Aadhaar
    adhaar_response = verify_adhaar_with_api(payload.adhaar_number)
    
    if adhaar_response.get("status_code") == 200 or adhaar_response.get("sub_code") == "INVALID_AADHAAR_NUMBER":
        raise HTTPException(status_code=400, detail="Aadhaar verification failed, Invalid adhaar number")
    elif adhaar_response.get("status") == "failed":
        raise HTTPException(status_code=400, detail="Aadhaar verification failed")

    # Step 2: Match last three digits of Aadhaar and phone number
    adhaar_last_three = adhaar_response.get("last_digits")
    phone_last_three = payload.phone_number[-3:]

    if adhaar_last_three != phone_last_three:
        raise HTTPException(status_code=400, detail="Phone number and Aadhaar mismatch")

    # Step 3: Generate OTP
    otp = random.randint(100000, 999999)
    store_otp(payload.phone_number, otp)

    # Step 4: Send OTP via Twilio
    send_otp_via_twilio(payload.phone_number, otp)

    return {"status": "ok", "message": "OTP sent successfully"}


@router.post("/user_signup_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"status": "ok", "message": "OTP verified successfully"}
