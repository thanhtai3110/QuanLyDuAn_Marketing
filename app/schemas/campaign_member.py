from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CampaignMemberBase(BaseModel):
    role: str

class CampaignMemberCreate(CampaignMemberBase):
    campaign_id: int
    user_id: int

class CampaignMemberUpdate(BaseModel):
    role: str 

class CampaignMemberResponse(CampaignMemberBase):
    campaign_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)