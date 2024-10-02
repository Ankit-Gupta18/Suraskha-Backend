from fastapi import FastAPI, HTTPException
from routers.login_signup import user_signup, police_signup, user_login, police_login
from routers.user_contacts_router import user_contacts_router
from routers.sos_utils import sos_router
from chat import chat
from routers import feedback_router
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse   # have to comment later

load_dotenv()
app = FastAPI(
    title="Suraksha Backend API",  # Custom title for the API
    description="API for Suraksha Backend Server, providing user sign-up, feedback, and contacts management functionalities.",
    version="1.0.0",  # API version
    docs_url="/docs",  # Custom Swagger docs path (optional, default is `/docs`)
    redoc_url="/redoc"  # Custom ReDoc path (optional, default is `/redoc`)
)

# Include the routers
app.include_router(user_signup.router)
app.include_router(police_signup.router)
app.include_router(user_login.router)
app.include_router(police_login.router)
app.include_router(user_contacts_router.router)
app.include_router(feedback_router.router)
app.include_router(chat.router)
app.include_router(sos_router.router)


# Serve the index.html at the root
# have to comment later
@app.get("/chat", response_class=HTMLResponse)
async def get_index():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Suraksha Backend Server!"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






