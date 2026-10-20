

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt
from pwdlib import PasswordHash
from fastapi import HTTPException
from pwdlib import PasswordHash

from models.user_model import UserModel
from repository.auth_repo import AuthRepository
from routes.request_response_model.auth_request import UserCreate


# Set SECRET_KEY in your environment before starting the app.
SECRET_KEY = "asdfasdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

password_hash = PasswordHash.recommended()

class AuthService:
  
  def __init__(self, repo: AuthRepository):
     self.repo = repo
     
  def create_user(self, user: UserCreate):

    h_password = password_hash.hash(user.password)
    user = self.repo.create(email=user.email, username=user.username, hash_password=h_password)
    # user_object = UserResponseDTO(id=user.id, username=user.username, email=user.email, is_active=user.is_active)

  
  def login_user(self, email: str, password: str) -> UserModel | None:
    
    
      user = self.repo.get_user(email)

      if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )
      
      print(f"====> {password} __ {user.hashed_password}")
      
      if not password_hash.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password ---",
        )
          
      expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      payload = {
          "sub": email,
          "exp": expires_at,
      }
      return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)