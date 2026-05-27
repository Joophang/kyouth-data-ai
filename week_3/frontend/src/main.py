from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

backend_url = os.getenv("BACKEND_URL")

@app.get("/")
def landing_page(request: Request):
	
	print(f"Backend URL from environment variable: {backend_url}")
	return templates.TemplateResponse(request=request,
								   name="chat_page.html",
								   context={"backend_url": backend_url})


