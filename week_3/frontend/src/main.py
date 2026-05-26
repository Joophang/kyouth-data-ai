from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def landing_page(request: Request):
	return templates.TemplateResponse(request=request, name="chat_page.html")
