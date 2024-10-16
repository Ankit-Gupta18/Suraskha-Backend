from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
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

@router.post("/police_login_send_otp")
async def user_login_send_otp(payload: OTPRequest):
    if db_manager.get_police_by_phone(payload.phone_number):
        # Step 1: Generate OTP
        otp = random.randint(100000, 999999)
        store_otp(payload.phone_number, otp)

        # Step 2: Send OTP via Twilio
        send_otp_via_twilio(payload.phone_number, otp)
    else:
        return {"status": "ok", "message": "User not registered, please register first!"}

    return {"status": "ok", "message": "User verified, OTP sent!"}


@router.post("/police_signin_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return JSONResponse(content={"message": "User verified!"}, status_code=200)
    
@router.post("/police_details")
async def get_police_details(payload: PhoneNumberRequest):
    try:
        # Extract the phone number from the request body
        phone_number = payload.phone_number

        # Fetch police details using the phone number
        police = db_manager.get_police_by_phone(phone_number)

        if not police:
            raise HTTPException(status_code=404, detail="User not found")

        # Returning the police details as a response
        return {
            "status": "success",
            "data": {
                "name": police.get("name"),
                "police_id": police.get("police_id"),
                "police_station_address": police.get("police_station_address"),
                "id_card": police.get("id_card"),
                "phone_number": police.get("phone_number"),
                "email": police.get("email"),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")