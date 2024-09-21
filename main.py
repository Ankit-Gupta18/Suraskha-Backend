from fastapi import FastAPI, HTTPException
from routers.login_signup import user_signup, police_signup
from routers.user_contacts_router import user_contacts_router
from routers import feedback_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(user_signup.router)
app.include_router(police_signup.router)
app.include_router(user_contacts_router.router)
app.include_router(feedback_router.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Suraksha Backend Server!"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






