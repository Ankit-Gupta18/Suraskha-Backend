import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# External Aadhaar verification function
def verify_adhaar_with_api(adhaar_number: str) -> dict:
    # Get API key from environment variables
    api_key = os.getenv("DEEPVUE_ADHAAR_API_KEY")
    client_id = os.getenv("DEEPVUE_CLIENT_ID")

    url_authorize = f"https://production.deepvue.tech/v1/authorize"
    form_data = {
        "client_id": client_id,
        "client_secret": api_key
    }

    response = requests.post(url_authorize, data=form_data)

    # Check response status and handle it
    if response.status_code == 200:
        response_data = response.json()  # Parse JSON response
        access_token = response_data.get("access_token")
    else:
        print("Failed:", response.status_code, response.text)


    url = f"https://production.deepvue.tech/v1/verification/aadhaar?aadhaar_number={adhaar_number}"
    headers = {
        "x-api-key": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Expected response format from API
    else:
        return {"status": "failed", "error": response.text}
