from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import pandas as pd
from pydantic import BaseModel
import joblib

app = FastAPI()

data_frame_columns = ['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
       'Sleep Hours', 'Sample Question Papers Practiced']

CurrentStudent = None
student = None

pipeline = joblib.load("models/RandomForest.joblib")

class Student(BaseModel):
    Hours_Studied: int
    Previous_Score : int
    Extracurricular_Activities: int
    Sleep_Hours : int
    Sample_Question_Papers_Practiced: int

# Serve static files (css, imgs, gifs)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point to templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request, "title": "Home"})

@app.get("/certificates", response_class=HTMLResponse)
async def certificate_page(request: Request):
    return templates.TemplateResponse("certificates/certificates.html", {"request": request, "title": "Certificates"})

@app.get("/projects/{project_name}", response_class=HTMLResponse)
async def project_page(request: Request, project_name: str, prediction: str = None):
    return templates.TemplateResponse(f"projects/{project_name}.html", {"request": request, "prediction": prediction, "student" : student, "title": project_name.replace("_", " ").title()})

@app.post('/predict', response_class=RedirectResponse)
def predict(request: Request, Hours_Studied: int = Form(...), Previous_Score: int = Form(...), Extracurricular_Activities: int = Form(...), Sleep_Hours: int = Form(...), Sample_Question_Papers_Practiced: int = Form(...), project_name: str = Form(...)):
    global student
    student = Student(
        Hours_Studied=Hours_Studied,
        Previous_Score=Previous_Score,
        Extracurricular_Activities=Extracurricular_Activities,
        Sleep_Hours=Sleep_Hours,
        Sample_Question_Papers_Practiced=Sample_Question_Papers_Practiced
    )

    input_data = pd.DataFrame([student.model_dump().values()], columns=data_frame_columns)
    prediction = pipeline.predict(input_data)[0]
    redirect_url = f"/projects/{project_name}?prediction={prediction}"
    return RedirectResponse(redirect_url, status_code=302)