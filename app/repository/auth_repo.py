


from fastapi import HTTPException
from requests import Session
from app.models.user_model import  UserModel


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def is_exist(self, email: str):
        existing_user = (
            self.db.query(UserModel)
            .filter(
                # (UserModel.username == user.username) |
                (UserModel.email == email)
            )
            .first()
        )
        return existing_user
        
        
    def create(self, email: str, username: str, hash_password: str):
        existing_user = self.is_exist(email)
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username or email already exists"
            )
        
        user = UserModel(
            username=username,
            email=email,
            hashed_password=hash_password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
    
    def get_user(self, email: str):
        # user = self.db.scalar(
        #     select(UserModel).where(UserModel.email == email)
        # )
        
        existing_user = self.is_exist(email)
        return existing_user
        
        # if existing_user is None:
        #     raise HTTPException(
        #         status_code=401,
        #         detail="Invalid username or password",
        #     )
        