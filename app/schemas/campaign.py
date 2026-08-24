from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# ==========================
# ĐỊNH NGHĨA ENUM CHUẨN DB
# ==========================
class MemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


# ==========================
# SCHEMA CHO CHIẾN DỊCH (CAMPAIGN)
# ==========================
class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass  # Dùng luôn các trường của Base để tạo


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================
# SCHEMA CHO THÀNH VIÊN (MEMBER)
# ==========================

# Khuôn hứng ID khi Owner muốn thêm thành viên mới
class CampaignMemberAdd(BaseModel):
    user_id: int


# Khuôn trả về thông tin thành viên
class CampaignMemberResponse(BaseModel):
    campaign_id: int
    user_id: int
    role: MemberRole
    joined_at: datetime

    class Config:
        from_attributes = True