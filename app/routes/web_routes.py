"""Web routes for HTML pages."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, tags=["web"])
async def index(request: Request):
    """Home page with email and SMS test forms."""
    return templates.TemplateResponse("index.html", {"request": request})

