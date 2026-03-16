from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    ip = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    url = relationship("URL")