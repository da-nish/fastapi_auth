
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from dependency.user_validate import get_current_user
from models.user_model import UserModel
from repository.auth_repo import AuthRepository
from routes.request_response_model.auth_request import UserCreate, UserLogin
from service.auth_service import AuthService
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/create")
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    
    repo = AuthRepository(db=db)
    service = AuthService(repo=repo)
    service.create_user(user=body)

    return {"message": "Created successfully !!"}


@router.post("/login")
def login(body: UserLogin, db: Session = Depends(get_db)):
   
    repo = AuthRepository(db=db)
    service = AuthService(repo=repo)
    
    jwt_data = service.login_user(email=body.email,password= body.password)
    
    return {
        "id": "user_object.id",
        "token": jwt_data
    }


@router.get("/secure")
def secure_endpoint(username: Annotated[str, Depends(get_current_user)]):
    return {
        "message": "Access granted",
        "user": username,
        "data": "This is confidential information",
    }