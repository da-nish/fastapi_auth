

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from database.database import get_db
from dependency.user_validate import get_current_user
from dto.auth_dto import UserDTO
from models.user_model import UserModel
from service.auth_service import AuthService
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Set SECRET_KEY in your environment before starting the app.
SECRET_KEY = "asdfasdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/users")
def create_user(body: UserCreate, db: Session = Depends(get_db)):
   
    
    h_password = password_hash.hash(body.password)
    user = UserDTO(username=body.username, email=body.email, password=body.password, hashed_password=h_password)
    
    service = AuthService(db=db)
    user_object = service.create_user(user=user)

    return {
        "id": user_object.id,
        "username": user_object.username,
        "email": user_object.email,
        "is_active": user_object.is_active
    }


@router.post("/login")
def login(body: UserLogin, db: Session = Depends(get_db)):
   
    
    service = AuthService(db=db)
    user_object = service.login_user(body.email)
    
    print(user_object.email)
    
    if not password_hash.verify(
        body.password,
        user_object.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password ---",
        )
    
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_object.username,
        "exp": expires_at,
    }
    
    return {
        "id": "user_object.id",
        "token": jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM),
        "username": user_object.username,
        "email": user_object.email,
        "is_active": user_object.is_active
    }


@router.get("/secure")
def secure_endpoint(
    username: Annotated[str, Depends(get_current_user)],
):
    return {
        "message": "Access granted",
        "user": username,
        "data": "This is confidential information",
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()