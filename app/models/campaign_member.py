from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from app.db.database import Base

class CampaignMember(Base):
    __tablename__ = "campaign_members"

    campaign_id = Column(Integer,ForeignKey("campaigns.id"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    role = Column(Enum("OWNER", "MEMBER"),nullable=False)
    joined_at = Column(DateTime,default=datetime.utcnow,nullable=False)