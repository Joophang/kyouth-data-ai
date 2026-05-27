from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from week_2.prompt_model import prompt_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    pdf_text: str = ""

@app.post("/chat")
async def chat(request: ChatRequest):

    full_prompt = f"""
User message:
{request.message}

Resume content:
{request.pdf_text}
"""
    # print(f"Received chat request with message: {request.message} and PDF text : {request.pdf_text}")
    try:
        reply = prompt_model(model="gemini-2.5-flash-lite", prompt=full_prompt)

        return {
            "reply": reply
        }

    except Exception as e:
        return {
            "reply": f"Backend error: {str(e)}"
        }