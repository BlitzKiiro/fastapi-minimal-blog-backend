from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.database import Base
from utils.uuid import get_uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=get_uuid)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    blogs = relationship("Blog", back_populates="author", lazy="dynamic" )
    def __str__(self):
        return f"{self.id} {self.username} {list(map(lambda blog: f'{blog.title} {blog.body}' , self.blogs))}"
  
  
