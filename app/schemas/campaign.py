from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CampaignBase(BaseModel):
    name: str
    description: str 

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: str 
    description: str 
class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)