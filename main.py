from fastapi import FastAPI, HTTPException
from routers import adhaar_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(adhaar_router.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Suraksha Backend Server!"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






