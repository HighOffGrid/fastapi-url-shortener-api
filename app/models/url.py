from  sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database.connection import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    click_count = Column(Integer, default=0)
    def __repr__(self):        return f"<URL(id={self.id}, original_url='{self.original_url}', short_code='{self.short_code}', click_count={self.click_count})>"
    def to_dict(self):        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "click_count": self.click_count
    }