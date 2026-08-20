from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CampaignTaskBase(BaseModel):
    title: str
    description: str 
    assignee_id: int 
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime 


class CampaignTaskCreate(CampaignTaskBase):
    campaign_id: int


class CampaignTaskUpdate(BaseModel):
    title: str 
    description: str 
    assignee_id: int 
    status: TaskStatus 
    priority: TaskPriority 
    due_date: datetime 


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)