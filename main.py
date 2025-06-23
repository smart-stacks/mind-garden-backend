import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
from dotenv import load_dotenv

# Get the directory where main.py is located
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
# Load .env file from the project root
load_dotenv(BASE_DIR / ".env")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app

# Import the routers
from auth import router as auth_router
from chat_api import router as chat_router

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example session DB URL (e.g., SQLite)
# SESSION_DB_URL = "sqlite:///./sessions.db"
# Set up CORS allowed origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vite default development server
    "http://localhost:8080",  # Backend URL when running locally
    "https://mindgarden-6xntrakg7q-nw.a.run.app",  # Cloud Run backend URL
    os.getenv("FRONTEND_URL", "https://mindgarden-app-431880575932.europe-west2.run.app")  # Production frontend
]

# Log environment variables for debugging
logger.info(f"FRONTEND_URL: {os.getenv('FRONTEND_URL', 'Not set')}")
logger.info(f"REDIRECT_URI: {os.getenv('REDIRECT_URI', 'Not set')}")
logger.info(f"Allowed origins: {ALLOWED_ORIGINS}")

# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# Call the function to get the FastAPI app instance
# Ensure the agent directory name ('capital_agent') matches your agent folder
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=600
)

# Include the routers
app.include_router(auth_router)
app.include_router(chat_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Mind Garden Backend is Running"}


# You can add more FastAPI routes or configurations below if needed
# Example:
# @app.get("/hello")
# async def read_root():
#     return {"Hello": "World"}

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))