from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict

class CampaignBase(BaseModel):
    name: str
    description: str | None = None

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignMemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class CampaignMemberBase(BaseModel):
    role: CampaignMemberRole


class CampaignMemberCreate(CampaignMemberBase):
    campaign_id: int
    user_id: int


class CampaignMemberUpdate(BaseModel):
    role: CampaignMemberRole


class CampaignMemberResponse(CampaignMemberBase):
    campaign_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)