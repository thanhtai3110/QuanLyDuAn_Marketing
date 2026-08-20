from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CampaignTaskBase(BaseModel):
    title: str
    description: str 
    assignee_id: int 
    status: str
    priority: str
    due_date: datetime 

class CampaignTaskCreate(CampaignTaskBase):
    campaign_id: int

class CampaignTaskUpdate(BaseModel):
    title: str 
    description: str 
    assignee_id: int 
    status: str 
    priority: str 
    due_date: datetime 

class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)