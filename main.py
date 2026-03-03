from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TaskFlow API",
    description="To-Do List Backend API",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: change to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
