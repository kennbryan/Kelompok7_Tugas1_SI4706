from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class LoginOut(BaseModel):
    access_token: str

class ProfileIn(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    def dict_non_none(self):
        return {k: v for k, v in self.dict().items() if v is not None}

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]