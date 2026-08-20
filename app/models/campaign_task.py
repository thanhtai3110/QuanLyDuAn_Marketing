from datetime import datetime, timezone

from sqlalchemy import (Column,Integer,String,Text,Enum,DateTime,ForeignKey)

from app.db.database import Base
class CampaignTask(Base):
    __tablename__ = "campaign_tasks"

    id = Column(Integer,primary_key=True,autoincrement=True)

    campaign_id = Column(Integer,ForeignKey("campaigns.id"),nullable=False)

    title = Column(String(255),nullable=False)

    description = Column(Text,nullable=True)

    assignee_id = Column(Integer,ForeignKey("users.id"),nullable=True)

    status = Column(Enum("TODO", "IN_PROGRESS", "DONE"),default="TODO",nullable=False)

    priority = Column(Enum("LOW", "MEDIUM", "HIGH"),default="MEDIUM",nullable=False)

    due_date = Column(DateTime,nullable=True)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)