from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import base64
import requests
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

FOFA_EMAIL = os.getenv("FOFA_EMAIL") or "your_email@example.com"
FOFA_KEY = os.getenv("FOFA_KEY") or "your_fofa_api_key"

def get_fofa_url(query):
    b64_query = base64.b64encode(query.encode()).decode()
    return f"https://fofa.info/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={b64_query}&size=100"

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, query: str = Form(...)):
    try:
        url = get_fofa_url(query)
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        results = [d['link'] if d['link'] else d['host'] for d in data["results"]]
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": results,
            "query": query
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })