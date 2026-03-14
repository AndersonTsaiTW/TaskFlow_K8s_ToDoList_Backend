import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.database import Base, engine
from app.models.user import User
from app.models.todo import Todo
from app.api.v1.endpoints import todos, auth

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]


def get_allowed_origins() -> list[str]:
    origins = os.getenv("ALLOWED_ORIGINS")
    if not origins:
        return DEFAULT_ALLOWED_ORIGINS
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


def ensure_todo_user_column() -> None:
    """Backfill the schema change for existing local/dev databases."""
    inspector = inspect(engine)
    if "todos" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)
        return

    todo_columns = {column["name"] for column in inspector.get_columns("todos")}
    if "user_id" in todo_columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE todos ADD COLUMN user_id VARCHAR"))
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_todos_user_id ON todos (user_id)"
            )
        )
        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_todos_user_id_users'
                    ) THEN
                        ALTER TABLE todos
                        ADD CONSTRAINT fk_todos_user_id_users
                        FOREIGN KEY (user_id) REFERENCES users (id);
                    END IF;
                END $$;
                """
            )
        )

app = FastAPI(
    title="TaskFlow API",
    description="To-Do List Backend API",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_todo_user_column()


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API"}


# Kubernetes health check probes
@app.get("/healthz")
def liveness():
    """Liveness probe - checks if application is running"""
    return {"status": "ok"}


@app.get("/readyz")
def readiness():
    """Readiness probe - checks if application is ready to serve traffic"""
    return {"status": "ready"}


app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

app.include_router(
    todos.router,
    prefix="/api/v1",
    tags=["todos"]
)
