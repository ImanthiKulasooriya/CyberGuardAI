from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from . import models

from .routers import predictions
from .routers import events
from .routers import alerts
from .routers import dashboard
from .routers import reports


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CyberGuard AI",
    description="AI-Based Cybersecurity Threat Detection System",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# API routers
app.include_router(predictions.router)
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)
app.include_router(reports.router)