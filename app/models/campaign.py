from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.db.database import Base
class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )