"""
Vobiz Voice AI Platform - Main Entry Point
Built for Indian Dental Clinics with Gemini 2.5 Live
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
from .config import settings
from .routes import calls, webhooks, analytics

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting Vobiz Voice AI Platform", 
                environment=settings.APP_ENV,
                port=settings.SERVER_PORT)
    # Startup: Initialize connections
    yield
    # Shutdown: Cleanup connections
    logger.info("Shutting down Vobiz Voice AI Platform")

app = FastAPI(
    title="Vobiz Voice AI Platform",
    description="AI-powered voice calling for dental clinics in India",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(calls.router, prefix="/api/v1/calls", tags=["Calls"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    return {
        "name": "Vobiz Voice AI Platform",
        "version": "1.0.0",
        "status": "running",
        "target_market": "Indian Dental Clinics"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "voice-agent",
        "timestamp": "2024-01-15T10:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=(settings.APP_ENV == "development")
    )
