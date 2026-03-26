# TaskFlow_K8s_ToDoList_Backend

A FastAPI-based To-Do List backend application designed for Kubernetes deployment.

## Documentation

### CI/CD & Deployment
- **[CI/CD Pipeline Setup](docs/ci-cd-pipeline.md)** - Overall architecture and workflow
  - [GitHub Actions Setup Guide](docs/cicd-github-actions-setup.md) - GitHub repository configuration
  - [IAM Role Setup](docs/cicd-github-actions-ecr-push-role.md) - AWS configuration details

### Database
- [Database Migrations](docs/database-migrations.md) - Alembic setup and workflow

---

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Pydantic** - Data validation and settings management
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL** - Production database
- **Docker & Docker Compose** - Containerization
- **Kubernetes** - Container orchestration (deployment target)

## Project Structure

```
TaskFlow_K8s_ToDoList_Backend/
├── app/
│   ├── api/          # API routes and endpoints
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic schemas for validation
│   ├── services/     # Business logic layer
│   └── database.py   # Database connection and session
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker image configuration
├── docker-compose.yml # Multi-container orchestration
├── .env              # Environment variables (local)
├── .env.example      # Environment variables template
├── .dockerignore     # Docker ignore patterns
└── .gitignore        # Git ignore patterns
```

## Getting Started

### Prerequisites

- Python 3.11+ (3.13 recommended)
- Docker Desktop
- PostgreSQL (via Docker, included in docker-compose)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskFlow_K8s_ToDoList_Backend
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env if needed (default values work for local development)
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Start the database**
   ```bash
   # Start only PostgreSQL in Docker
   docker-compose up db
   ```

7. **Run database migrations**
   ```bash
   # Initialize Alembic (only needed once, already done)
   # alembic init alembic
   
   # Create a new migration (after modifying models)
   alembic revision --autogenerate -m "Description of changes"
   
   # Apply migrations to database
   alembic upgrade head
   ```

8. **Run the development server** (in a new terminal)
   ```bash
   # With virtual environment activated
   uvicorn main:app --reload
   ```

9. **Access the application**
   - API: <http://localhost:8000>
   - Interactive API docs (Swagger UI): <http://localhost:8000/docs>
   - Alternative API docs (ReDoc): <http://localhost:8000/redoc>

## Database Migrations

This project uses **Alembic** for database schema versioning and migrations.

### Understanding Alembic

Alembic is like Git for your database schema:
- Tracks changes to database structure over time
- Allows upgrading/downgrading database versions
- Ensures team members have consistent database schemas
- Essential for production deployments

### Common Migration Workflows

#### Initial Setup (Already Configured)

```bash
# Initialize Alembic (creates alembic/ folder and alembic.ini)
alembic init alembic

# Configure alembic/env.py to import your models
# Configure alembic.ini database connection
```

#### Creating Migrations After Model Changes

1. **Modify your models** (e.g., `app/models/todo.py`)
   ```python
   class Todo(Base):
       # ... existing fields
       is_urgent = Column(Boolean, default=False)  # New field
   ```

2. **Generate migration**
   ```bash
   alembic revision --autogenerate -m "Add is_urgent field to todos"
   ```
   This creates a file in `alembic/versions/` with upgrade/downgrade SQL.

3. **Review the generated migration**
   ```bash
   # Check the generated file in alembic/versions/
   # Ensure the SQL looks correct
   ```

4. **Apply migration**
   ```bash
   alembic upgrade head
   ```

#### Useful Migration Commands

```bash
# View current migration version
alembic current

# View migration history
alembic history

# Upgrade to latest version
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# View SQL without executing (dry-run)
alembic upgrade head --sql
```

### Migration in Docker

#### Option 1: Manual Execution (Recommended for Production)

```bash
# Run migration in running container
docker exec <container_name> alembic upgrade head

# Or with docker-compose
docker-compose exec backend alembic upgrade head
```

#### Option 2: Auto-run on Startup (Development/Testing)

Add to your Docker entrypoint script:
```bash
#!/bin/bash
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Option 3: Kubernetes Init Container

```yaml
initContainers:
- name: migration
  image: your-backend-image
  command: ["alembic", "upgrade", "head"]
  env:
    - name: DATABASE_URL
      value: "postgresql://..."
```

### Migration Best Practices

- ✅ **Always review** auto-generated migrations before applying
- ✅ **Test migrations** on development database first
- ✅ **Commit migration files** to version control
- ✅ **Never modify** applied migrations (create new ones instead)
- ✅ **Backup production data** before major migrations
- ⚠️ **Avoid** data loss operations (dropping columns with data)

## Environment Variables

Key environment variables (see `.env.example` for full list):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://taskflow:password@localhost:5432/taskflow` |
| `ENV` | Environment (development/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `PORT` | API server port | `8000` |

## API Endpoints

### Health Check Endpoints

- `GET /` - Welcome message
- `GET /healthz` - Liveness probe (for Kubernetes)
- `GET /readyz` - Readiness probe (for Kubernetes)

### Todo Endpoints

#### Implemented

- `GET /api/v1/todos` - List todos with filtering and sorting
  - Query parameters: `status`, `q` (search), `tag`, `due_from`, `due_to`, `priority`, `sort_by`, `order`
- `POST /api/v1/todos` - Create a new todo
  - Body: `title` (required), `description`, `due_at`, `priority`, `tags`

#### Coming Soon

- `GET /api/v1/todos/{id}` - Get todo by ID
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo
- `PATCH /api/v1/todos/{id}` - Partially update todo

## Development Workflow

### Method 1: Local Development (Recommended for Active Development)

**Advantages**: Fast hot-reload, easy debugging, IDE integration

```bash
# Terminal 1: Start database only
docker-compose up db

# Terminal 2: Run API locally with hot-reload
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
uvicorn main:app --reload
```

**Database Connection**: Uses `.env` configuration (`localhost:5432`)

### Method 2: Full Docker Development

**Advantages**: Production-like environment, tests container integration

```bash
# Start both API and database containers
docker-compose up --build

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

**Database Connection**: Uses `docker-compose.yml` override (`db:5432`)

### Database Management

```bash
# Access PostgreSQL database
docker exec -it taskflow-db psql -U taskflow -d taskflow

# View database logs
docker logs taskflow-db

# Reset database (removes all data)
docker-compose down -v
docker-compose up db
```

## Deployment

This application is designed to be deployed on Kubernetes. Docker images can be built using the included Dockerfile.

### Building and Running Docker Container

```bash
# Build Docker image
docker build -t taskflow-api:latest .

# Run migration (before starting the app)
docker run --rm taskflow-api:latest alembic upgrade head

# Run the container
docker run -p 8000:8000 taskflow-api:latest
```

### Deployment Checklist

1. **Update environment variables** for production
2. **Run database migrations**
   ```bash
   # In production environment
   alembic upgrade head
   ```
3. **Build and push Docker image**
   ```bash
   docker build -t your-registry/taskflow-api:v1.0.0 .
   docker push your-registry/taskflow-api:v1.0.0
   ```
4. **Deploy to Kubernetes** (manifests coming soon)
5. **Verify health endpoints**
   - `/healthz` - Liveness probe
   - `/readyz` - Readiness probe

## License

This project is licensed under the MIT License.
