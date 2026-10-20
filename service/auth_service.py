


from fastapi import HTTPException
from requests import Session
from sqlalchemy import select

from dto.auth_dto import UserDTO, UserResponseDTO
from models.user_model import  UserModel


class AuthService:
  
  def __init__(self, db: Session):
     self.db = db
     
  def create_user(self, user: UserDTO) -> UserResponseDTO:
    print(user.username)
    existing_user = (
      self.db.query(UserModel)
      .filter(
          (UserModel.username == user.username) |
          (UserModel.email == user.email)
      )
      .first()
  )
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password
    )

    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    
    
    user_object = UserResponseDTO(id=user.id, username=user.username, email=user.email, is_active=user.is_active)

    return user_object
  
  def login_user(self, email: str) -> UserModel | None:

      user = self.db.scalar(
        select(UserModel).where(UserModel.email == email)
      )
      
      if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )
  
      return user