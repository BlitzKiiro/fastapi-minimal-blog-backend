from pydantic import BaseModel, Field
from typing import Optional, List
from .blog import BlogResponse

class UserCreate(BaseModel):
    username: str = Field(..., description="user name")
    password: str = Field(..., description="user password")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="user name")
    password: Optional[str] = Field(None, description="user password")

class UserLogin(BaseModel):
    username: str = Field(..., description="user name")
    password: str = Field(..., description="user password")

class UserResponse(BaseModel):
    id: str = Field(..., description="user id")
    username: str = Field(..., description="user name")
    blogs: List[BlogResponse]  = Field(..., description="user blogs")
    class config:
        orm_mode = True
      