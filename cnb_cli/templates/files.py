# ----------------------------
# Main FastAPI Application
# ----------------------------
MAIN_PY = """\
from fastapi import FastAPI
from app.routers.health import router as health_router
from app.core.config import settings
from loguru import logger

# Optional: Import middleware or exception handlers
# from app.middleware.audit import AuditMiddleware
# from app.exception.handler import ExceptionHandlers

app = FastAPI(title="CNB FastAPI App")

# Include Routers
app.include_router(health_router)

# Optional: Add middleware
# app.add_middleware(AuditMiddleware)

# Optional: Add exception handlers
# handlers = ExceptionHandlers()
# app.add_exception_handler(Exception, handlers.global_exception_handler)

# Startup / Shutdown events
@app.on_event("startup")
async def on_startup():
    logger.info("FastAPI application startup")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("FastAPI application shutdown")
"""

# ----------------------------
# Application Configuration
# ----------------------------
CONFIG_PY = """\
from pydantic_settings import BaseSettings
# from app.utils.encryption import decrypt_data

class AppConfig(BaseSettings):
    # key: str = ""  # Optional encryption key
    enable_log_request_header: bool = True
    enable_log_request_body: bool = True
    debug_mode: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

    # def __init__(self, **values):
    #     super().__init__(**values)
    #     self.enable_log_request_header = decrypt_data(self.enable_log_request_header, self.key)
    #     self.enable_log_request_body = decrypt_data(self.enable_log_request_body, self.key)

settings = AppConfig()
"""

# ----------------------------
# Encryption Utilities
# ----------------------------
ENCRYPTION_PY = """\
from cryptography.fernet import Fernet, InvalidToken

def is_encrypted(value: str) -> bool:
    return value.startswith('gAAAAAB')

def decrypt_data(value: str, key: str):
    if not value or not key or not is_encrypted(value):
        return value
    try:
        cipher = Fernet(key.encode())
        return cipher.decrypt(value.encode()).decode()
    except InvalidToken:
        return value

def encrypt_data(value: str, key: str):
    if not value or not key:
        return value
    cipher = Fernet(key.encode())
    return cipher.encrypt(value.encode()).decode()
"""

# ----------------------------
# Health Router
# ----------------------------
HEALTH_ROUTER = """\
from fastapi import APIRouter

router = APIRouter()

@router.get("/health/")
def health_check():
    return {"status": "ok"}
"""

# ----------------------------
# Default Environment File
# ----------------------------
ENV_FILE = """\
ENABLE_LOG_REQUEST_HEADER=true
ENABLE_LOG_REQUEST_BODY=true
DEBUG_MODE=false
"""

# ----------------------------
# Default Requirements
# ----------------------------
REQUIREMENTS = """\
fastapi           
uvicorn           
gunicorn          
cryptography      
pydantic-settings 
httpx             
typer             
rich              
questionary       
openpyxl          
playwright        
loguru
cli          
"""


# ----------------------------
# Default README.md
# ----------------------------
README_MD = """\
# My FastAPI App

## Folder Structure

- `app/` : Main application code
    - `main.py` : FastAPI entry point
    - `config.py` : Configuration and environment variables
    - `core/` : Core utilities like security and app settings
    - `db/` : Database setup (only if DB connection enabled)
    - `models/` : ORM models
    - `schemas/` : Pydantic request/response models
    - `routers/` : API route definitions
    - `services/` : Business logic
    - `utils/` : Helper functions, e.g., encryption
- `tests/` : Unit and integration tests
- `requirements.txt` : Python dependencies
- `.env` : Environment variables
- `Dockerfile` : Docker setup for containerized deployment
- `pip.conf` : Pip configuration (optional)

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\\Scripts\\activate    # Windows

"""

# ----------------------------
# Default pip.conf
# ----------------------------
PIP_CONF = """\
[global]
index = https://nexus-mirror.xxx.com/repository/pypi-proxy/pypi
index-url = https://nexus-mirror.xxx.com/repository/pypi-proxy/simple
extra-index-url = https://nexus-mirror.xxx.com/repository/pypi-public-repo/simple
trusted-host = nexus-mirror.xxx.com
"""
