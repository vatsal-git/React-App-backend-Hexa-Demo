from pydantic import BaseModel
from api.schemas.user import UserInDB


class LoginData(BaseModel):
    access_token: str
    token_type: str
    user: UserInDB

    class Config:
        from_attributes = True
