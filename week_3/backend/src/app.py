from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
	prompt = await request.json()
	print(prompt)
	return prompt