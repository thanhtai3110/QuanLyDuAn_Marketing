from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, RoleChecker

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 1. Khu vực dành cho người đã đăng nhập
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# 2. Khu vực VIP chỉ dành cho ADMIN 
@router.get("", response_model=list[UserResponse])
def get_all_users(
    
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên hoặc email"),
    is_active: Optional[bool] = Query(None, description="Lọc theo trạng thái (true/false)"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(RoleChecker(["ADMIN"]))
):
    query = db.query(User)
    
    if search:
        query = query.filter(
            or_(
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)
        
    users = query.all()
    return users