from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files (css, imgs, gifs)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point to templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})

@app.get("/certificates", response_class=HTMLResponse)
async def certificate_page(request: Request):
    return templates.TemplateResponse("certificates/certificates.html", {"request": request})

@app.get("/{project_name}", response_class=HTMLResponse)
async def project_page(request: Request, project_name: str):
    return templates.TemplateResponse(f"projects/{project_name}.html", {"request": request})

