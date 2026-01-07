from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import models
import schemas
import database
from email_utils import EmailService
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize DB tables
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

# Get allowed origins from env, default to * for dev if not set.
# In production, set ALLOWED_ORIGINS=https://your-vercel-app.com,https://www.your-vercel-app.com
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

email_service = EmailService()


# Admin email to receive notifications
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

@app.post("/join", response_model=schemas.UserResponse)
async def join_waitlist(
    user: schemas.UserCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = models.User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send notification email if admin email is configured
    if ADMIN_EMAIL:
        background_tasks.add_task(
            email_service.send_notification_email, 
            new_user.email, 
            ADMIN_EMAIL
        )
    
    # Send welcome email to the new user
    background_tasks.add_task(email_service.send_welcome_email, new_user.email)
    
    return new_user


from fastapi import Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

api_key_query = APIKeyQuery(name="admin_secret", auto_error=False)
api_key_header = APIKeyHeader(name="X-Admin-Secret", auto_error=False)

def get_admin_secret(
    query_key: str = Security(api_key_query),
    header_key: str = Security(api_key_header),
):
    valid_secret = os.getenv("ADMIN_SECRET")
    if not valid_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Admin secret not configured on server"
        )
        
    if query_key == valid_secret or header_key == valid_secret:
        return valid_secret
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing admin secret"
    )

@app.get("/export")
def export_users(admin_secret: str = Depends(get_admin_secret)):
    db = database.SessionLocal()
    users = db.query(models.User).all()
    db.close()
    return [user.email for user in users]


@app.get("/")
def read_root():
    return {"message": "Waitlist API is running"}
