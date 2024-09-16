from fastapi import FastAPI, HTTPException
from routers.login import user_signup
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(user_signup.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Suraksha Backend Server!"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






