from datetime import datetime
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True)

    email = Column(String(255),unique=True,nullable=False)

    password_hash = Column(String(255),nullable=False)

    full_name = Column(String(255),nullable=False)

    role = Column(Enum("USER", "ADMIN"),default="USER",nullable=False)

    is_active = Column(Boolean,default=True,nullable=False)

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

    # User 1 - N Campaign
    owned_campaigns = relationship("Campaign",back_populates="owner")

    # User N - N Campaign
    # thông qua CampaignMember
    memberships = relationship("CampaignMember",back_populates="user")

    # User 1 - N CampaignTask
    assigned_tasks = relationship("CampaignTask",back_populates="assignee")