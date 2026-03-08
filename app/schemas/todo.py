from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class TodoCreate(BaseModel):
    """data format for creating Todo"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None)
    due_at: Optional[datetime] = Field(None)
    priority: int = Field(1, ge=1, le=5)
    tags: Optional[List[str]] = Field(None)


class TodoUpdate(BaseModel):
    """data format for updating Todo (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None)
    due_at: Optional[datetime] = Field(None)
    priority: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[List[str]] = Field(None)
    status: Optional[str] = Field(None)


class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: int
    position: int
    due_at: Optional[datetime]
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True

class TodoListResponse(BaseModel):
    items: List[TodoResponse]
    total: int