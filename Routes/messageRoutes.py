# Routes/messageRoutes.py
from fastapi import APIRouter
from Controllers.messageController import router as message_router

router = APIRouter()

router.include_router(message_router, prefix="/message")
