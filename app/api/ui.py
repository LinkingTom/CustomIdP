from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """Users management page"""
    return templates.TemplateResponse("users.html", {"request": request})


@router.get("/teams", response_class=HTMLResponse)
async def teams_page(request: Request):
    """Teams management page"""
    return templates.TemplateResponse("teams.html", {"request": request}) 