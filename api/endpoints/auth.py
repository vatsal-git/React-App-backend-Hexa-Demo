from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.auth import LoginData
from api.schemas.user import UserCreate, UserLogin
from core.database import get_db
from core.security import create_access_token, verify_password, get_password_hash
from typing import Annotated, Union

router = APIRouter()


@router.post("/register/", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username or User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    # Create new user
    new_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(data={"sub": new_user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/", response_model=LoginData)
def login_user(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
# def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    # Retrieve user from database
    db_user = db.query(User).filter(User.username == user_login.username).first()
    if not db_user or not verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer", "user": db_user}
