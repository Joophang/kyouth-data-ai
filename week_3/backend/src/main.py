from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from week_2.prompt_model import prompt_model
from week_2.find_skill_gaps import find_skill_gaps
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

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

def is_skill_gap_request(message: str) -> bool:
    message = message.lower()

    keywords = [
        "skill gap",
        "skill gaps",
        "missing skill",
        "missing skills",
        "gap analysis",
        "what skills am i missing",
        "skills missing",
    ]

    return any(keyword in message for keyword in keywords)


@app.post("/chat")
async def chat(request: ChatRequest):
    if (not request.message) and (not request.pdf_text):
        return {"reply": "Please provide a message or resume content."}
    try:

        if is_skill_gap_request(request.message) and request.pdf_text:
            db_url = BASE_DIR / "week_2" / "data" / "jobs_d3_eval.db"

            result = find_skill_gaps(
                resume_txt=request.pdf_text,
                db_url=str(db_url))

            return {
                "reply": f"Your skill gaps are: {', '.join(result.gaps)}"
            }

        if (request.message) and (not request.pdf_text):
            full_prompt = f"""User message:
            {request.message}
            """
            reply = prompt_model(
                model="gemini-2.5-flash-lite",
                prompt=full_prompt,
            )
            return {"reply": reply}

        full_prompt = f"""
            User message:
            {request.message}

            Resume content:
            {request.pdf_text}
            """

        reply = prompt_model(
            model="gemini-2.5-flash-lite",
            prompt=full_prompt,
        )

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Backend error: {str(e)}"}