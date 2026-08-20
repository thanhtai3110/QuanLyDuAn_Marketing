from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
class UserCreate(UserBase):
    password: str
class UserUpdate(BaseModel):
    full_name: str 
    is_active: bool 

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)