from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from routers.external.otp_service_twilio import send_otp_via_twilio
from routers.utils.otp_store_and_verify import store_otp, verify_otp
from db.dbmanager import DBManager
import random
db_manager = DBManager().get_instance()


router = APIRouter()


# Request payload model for OTP verification
class OTPRequest(BaseModel):
    phone_number: str

# Request payload model for OTP verification
class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

class PhoneNumberRequest(BaseModel):
    phone_number: str


@router.post("/user_login_send_otp")
async def user_login_send_otp(payload: OTPRequest):
    if db_manager.get_user_by_phone(payload.phone_number):
        # Step 1: Generate OTP
        otp = random.randint(100000, 999999)
        store_otp(payload.phone_number, otp)

        # Step 2: Send OTP via Twilio
        send_otp_via_twilio(payload.phone_number, otp)
    else:
        return {"status": "ok", "message": "User not registered, please register first!"}

    return {"status": "ok", "message": "User verified, OTP sent!"}


@router.post("/user_signin_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
@router.post("/user_details")
async def get_user_details(payload: PhoneNumberRequest):
    try:
        # Extract the phone number from the request body
        phone_number = payload.phone_number

        # Fetch user details using the phone number
        user = db_manager.get_user_by_phone(phone_number)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Returning the user details as a response
        return {
            "status": "success",
            "data": {
                "name": user.get("name"),
                "aadhaar_number": user.get("aadhaar_number"),
                "state": user.get("state"),
                "age_group": user.get("age_group"),
                "gender": user.get("gender"),
                "phone_number": user.get("phone_number"),
                "email": user.get("email"),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")