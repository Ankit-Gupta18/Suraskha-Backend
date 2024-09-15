from fastapi import APIRouter,HTTPException
import requests
from db.dbmanager import DBManager
import json

router = APIRouter()

# Define API route to verify adhaar
@router.get("/adhaar_verification")
async def verify_adhaar(sample_id: str):
    
    return {"status":"ok"}