from datetime import datetime, timezone
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer,primary_key=True,autoincrement=True)

    name = Column(String(255),nullable=False)

    description = Column(Text,nullable=True)

    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    created_at = Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)

    # User 1 - N Campaign
    owner = relationship("User",back_populates="owned_campaigns")

    # Campaign N - N User
    
    members = relationship("CampaignMember",back_populates="campaign")

    # Campaign 1 - N CampaignTask
    tasks = relationship("CampaignTask",back_populates="campaign")

class CampaignMember(Base):
    __tablename__ = "campaign_members"

    campaign_id = Column(Integer,ForeignKey("campaigns.id"),primary_key=True)

    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)

    role = Column(Enum("OWNER", "MEMBER"),nullable=False)

    joined_at = Column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)

    campaign = relationship("Campaign",back_populates="members")

    user = relationship("User",back_populates="memberships")