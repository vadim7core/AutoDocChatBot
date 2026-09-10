from fastapi import FastAPI
from pydantic import BaseModel

from app.ai_service import generate_reply
from app.services.lmstudio import classify_question

app = FastAPI(title="chatbot")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "online"}


@app.post("/chat")
def chat(request: ChatRequest):
    
    category = classify_question(request.message)

    print(f"CATEGORY: {category}")

    # Blochează întrebările non-auto
    if category == "NON_AUTO":
        return {
           "response": (
                    "Pot răspunde doar la întrebări legate de automobile: "
                    "diagnoză, întreținere, motoare, piese, modele și probleme tehnice."
                )
        }

    # Întrebare auto → DeepSeek
    reply = generate_reply(request.message)

    return {
        "response": reply
    }