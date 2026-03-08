from typing import Optional, List, Literal
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, Query
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import func, or_
from app.models.todo import Todo

router = APIRouter()

@router.get("/todos", response_model=TodoListResponse)
def list_todos(
  status: Optional[str] = Query(
    None,
    description="Filter by status: all, open, done, archived"
  ),
  q: Optional[str] = Query(
    None,
    description="Search keyword (searches in title and description)"
  ),
  tag: Optional[List[str]] = Query(
    None,
    description="Filter by tags (can specify multiple tags)"
  ),
  due_from: Optional[datetime] = Query(
    None,
    description="Due date range start (format: YYYY-MM-DDTHH:MM:SS)"
  ),
  due_to: Optional[datetime] = Query(
    None,
    description="Due date range end (format: YYYY-MM-DDTHH:MM:SS)"
  ),
  priority: Optional[int] = Query(
    None,
    ge=1,
    le=5,
    description="Filter by minimum priority (e.g., 3 returns priority >= 3: items with priority 3, 4, 5)"
  ),
  sort_by: Literal["created_at", "updated_at", "due_at", "priority", "title"] = Query(
    "created_at",
    description="Sort by field"
  ),
  order: Literal["asc", "desc"] = Query(
    "asc",
    description="Sort order (asc=ascending, desc=descending)"
  ),
  db: Session = Depends(get_db)
):
  query = db.query(Todo)

  if status and status != "all":
    query = query.filter(Todo.status == status)

  if q:
    search_pattern = f"%{q}%"
    query = query.filter(
      or_(
        Todo.title.ilike(search_pattern),
        Todo.description.ilike(search_pattern)
      )
    )
  
  if tag:
    for t in tag:
      query = query.filter(Todo.tags.contains([t]))
  if due_from:
    query = query.filter(Todo.due_at >= due_from)
  if due_to:
    query = query.filter(Todo.due_at <= due_to)
  if priority:
    query = query.filter(Todo.priority >= priority)

  sort_columns = {
    "title": Todo.title,
    "priority": Todo.priority,
    "due_at": Todo.due_at,
    "updated_at": Todo.updated_at,
    "created_at": Todo.created_at,
  } 
  order_column = sort_columns.get(sort_by, Todo.created_at)
  if order == "desc":
    query = query.order_by(order_column.desc())
  else:
    query = query.order_by(order_column.asc())

  todos = query.all()

  return {"items": todos, "total": len(todos)}
    
@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db)
):
  todo_id = str(uuid.uuid4())

  max_position = db.query(func.max(Todo.position)).scalar()
  new_position = (max_position or 0) + 1

  new_todo = Todo(
    id=todo_id,
    title=todo_data.title,
    description=todo_data.description,
    due_at=todo_data.due_at,
    priority=todo_data.priority,
    tags=todo_data.tags or [],
    position=new_position,
    status="open"
  )

  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)

  return new_todo
