# TaskFlow_K8s_ToDoList_Backend

A FastAPI-based To-Do List backend application designed for Kubernetes deployment.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Pydantic** - Data validation and settings management
- **Docker** - Containerization
- **Kubernetes** - Container orchestration (deployment target)

## Project Structure

```
TaskFlow_K8s_ToDoList_Backend/
├── app/
│   ├── api/          # API routes and endpoints
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── .dockerignore     # Docker ignore patterns
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop (optional, for containerized development)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskFlow_K8s_ToDoList_Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the development server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs (Swagger UI): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

### Docker Development

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Stop the container**
   ```bash
   # Press Ctrl+C in the terminal, or in a new terminal:
   docker-compose down
   ```

## API Endpoints

### Health Check Endpoints

- `GET /` - Welcome message
- `GET /healthz` - Liveness probe (for Kubernetes)
- `GET /readyz` - Readiness probe (for Kubernetes)

## Development Workflow

### Daily Development
Use the virtual environment for fast development with hot-reload:
```bash
.\venv\Scripts\Activate.ps1  # Activate virtual environment
uvicorn main:app --reload     # Run development server
```

### Testing with Docker
Periodically test with Docker to ensure deployment compatibility:
```bash
docker-compose up --build
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