from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from app.api.users import router as users_router
from app.api.teams import router as teams_router
from app.api.ui import router as ui_router

app = FastAPI(
    title="Lightweight IDP",
    description="A lightweight identity provider service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(ui_router)  # UI routes (no prefix for root pages)
app.include_router(users_router, prefix="/api")  # API routes with /api/users prefix
app.include_router(teams_router, prefix="/api")  # API routes with /api/teams prefix

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint"""
    return FileResponse("static/favicon.ico")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Lightweight IDP is running"}

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Welcome to Lightweight IDP API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "ui": "/"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 