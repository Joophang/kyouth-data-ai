from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

load_dotenv()

@app.get("/")
def landing_page(request: Request):
	backend_url = os.getenv("BACKEND_URL")
	return templates.TemplateResponse(request=request, name="chat_page.html")
