# middleware/errorMiddleware.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        return JSONResponse(content={"message": exc.detail}, status_code=exc.status_code)
    except Exception as exc:
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)
