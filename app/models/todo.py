"""
Todo database model
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class Todo(Base):
    """Todo table"""
    __tablename__ = "todos"

    # Primary key
    id = Column(String, primary_key=True)
    
    # Core fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="open", nullable=False)  # open, done, archived
    priority = Column(Integer, default=1, nullable=False)
    position = Column(Integer, nullable=False)
    
    # Optional fields
    due_at = Column(DateTime(timezone=True), nullable=True)
    tags = Column(JSON, default=list, nullable=True)  # use JSON to store
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Todo {self.id}: {self.title}>"