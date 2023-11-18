from pydantic import BaseModel, Field
from typing import Optional

class BlogCreate(BaseModel):
    title: str = Field(..., description="Title of the blog")
    body: str =  Field(..., description="Title of the blog")

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the blog")
    body: Optional[str] = Field(None, description="Body of the blog")

class BlogResponse(BaseModel):
    id: str = Field(..., description="Blog id")
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
    class config:
        orm_mode = True