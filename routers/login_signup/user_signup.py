from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers.external.verify_adhaar import verify_adhaar_with_api
from routers.external.otp_service_twilio import send_otp_via_twilio
from routers.utils.otp_store_and_verify import store_otp, verify_otp
import random
from db.dbmanager import DBManager
db_manager = DBManager().get_instance()

# Temporary store for signup details until OTP verification
signup_temp_store = {}

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
        return JSONResponse(content={"message": "User already exists"}, status_code=409)

    # Step 1: Verify Aadhaar
    adhaar_response = verify_adhaar_with_api(payload.adhaar_number)
    
    if adhaar_response.get("status_code") == 200 or adhaar_response.get("sub_code") == "INVALID_AADHAAR_NUMBER":
        return JSONResponse(content={"message": "Aadhaar verification failed, Invalid Aadhaar number"}, status_code=400)
    elif adhaar_response.get("status") == "failed":
        return JSONResponse(content={"message": "Aadhaar verification failed"}, status_code=400)

    # Step 2: Match last three digits of Aadhaar and phone number
    adhaar_last_three = adhaar_response.get("last_digits")
    phone_number_exists = adhaar_response.get("is_mobile")
    phone_last_three = payload.phone_number[-3:]

    #TODO:
    # gender = adhaar_response["data"]["gender"]
    

    if phone_number_exists and str(adhaar_last_three) != str(phone_last_three):
        return JSONResponse(content={"message": "Phone number and Aadhaar mismatch"}, status_code=400)

    # Step 3: Generate OTP
    otp = random.randint(100000, 999999)
    store_otp(payload.phone_number, otp)

    # Step 4: Send OTP via Twilio
    send_otp_via_twilio(payload.phone_number, otp)

    # Step 5: Store the user's details temporarily until OTP verification
    name = payload.name
    phone_number = payload.phone_number
    email = payload.email
    signup_temp_store[payload.phone_number] = {
        "name": name,
        "aadhaar_number": adhaar_response["data"]["aadhaar_number"],
        "state": adhaar_response["data"]["state"],
        "age_group": adhaar_response["data"]["age_range"],
        "gender": adhaar_response["data"]["gender"],
        "phone_number": phone_number,
        "email": email
    }

    return JSONResponse(content={"message": "OTP sent successfully"}, status_code=200)


@router.post("/user_signup_verify_otp")
async def verify_otp_route(payload: VerifyOTPRequest):
    # Step 1: Verify OTP
    if not verify_otp(payload.phone_number, payload.otp):
        if payload.phone_number in signup_temp_store:
            del signup_temp_store[payload.phone_number]  # Remove temp data on failure
        return JSONResponse(content={"message": "Invalid OTP"}, status_code=400)

    # Step 2: Fetch Aadhaar details and user details from the temporary store
    if payload.phone_number not in signup_temp_store:
        return JSONResponse(content={"message": "No signup data found for this phone number"}, status_code=400)

    user_details = signup_temp_store[payload.phone_number]
    del signup_temp_store[payload.phone_number]  # Remove after verification

    # Step 3: Add user data to DB
    db_payload = {
        "name": user_details["name"],
        "aadhaar_number": user_details["aadhaar_number"],
        "state": user_details["state"],
        "age_group": user_details["age_group"],
        "gender": user_details["gender"],
        "phone_number": payload.phone_number,
        "email": user_details["email"]
    }

    db_manager.insert_user_auth(db_payload)

    return JSONResponse(content={"message": "OTP verified and user added successfully"}, status_code=200)
