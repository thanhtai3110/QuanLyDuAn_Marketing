from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    """
    Dữ liệu đầu vào khi Đăng ký tài khoản.
    Bao gồm email, họ tên và mật khẩu thô.
    """
    password: str
class UserUpdate(BaseModel):
    full_name: str 
    is_active: bool 

class UserLogin(BaseModel):
    """
    Dữ liệu đầu vào khi Đăng nhập.
    Chỉ cần email và mật khẩu.
    """
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """
    Dữ liệu trả về cho client. 
    TUYỆT ĐỐI KHÔNG trả về mật khẩu, chỉ trả về các thông tin an toàn.
    """
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)