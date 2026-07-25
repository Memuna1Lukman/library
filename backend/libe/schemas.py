from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class TokenData(BaseModel):
    id: Optional[int]= None



class NewUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: Optional[int] = None 
    username: str
    email: EmailStr
    created_at : Optional[datetime] = None
    model_config = {"from_attributes": True}
   

class LogInUser(BaseModel):
    email: EmailStr 
    password: str    