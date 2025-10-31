"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router as api_router
from app.routes import web_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title="ClickSend Tester",
    description="Test email and SMS notifications via ClickSend API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(api_router)
app.include_router(web_routes.router)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    pass  # Static directory may not exist yet

