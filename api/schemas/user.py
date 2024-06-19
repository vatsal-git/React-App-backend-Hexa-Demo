
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[str] = 'user'


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDB(BaseModel):
    user_id: int
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    role: Optional[str] = 'user'

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
