# TaskFlow_K8s_ToDoList_Backend

A FastAPI-based To-Do List backend application designed for Kubernetes deployment.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Pydantic** - Data validation and settings management
- **SQLAlchemy** - SQL toolkit and ORM
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

7. **Run the development server** (in a new terminal)
   ```bash
   # With virtual environment activated
   uvicorn main:app --reload
   ```

8. **Access the application**
   - API: <http://localhost:8000>
   - Interactive API docs (Swagger UI): <http://localhost:8000/docs>
   - Alternative API docs (ReDoc): <http://localhost:8000/redoc>docs
   Environment Variables

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

### Todo Endpoints (Coming Soon)

- `GET /todos` - List all todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get todo by ID
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

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

```bash
# Build Docker image
docker build -t taskflow-api:latest .

# Run the container
docker run -p 8000:8000 taskflow-api:latest
```

## License

This project is licensed under the MIT License.
