from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
from utils.uuid import get_uuid

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(String, primary_key=True, default=get_uuid)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="blogs")
    def __str__(self):
        return f"{self.id} {self.title} {self.body}"