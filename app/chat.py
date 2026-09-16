from fastapi import FastAPI
from pydantic import BaseModel

import time
from threading import Lock

from app.ai_service import generate_reply
from app.services.lmstudio import classify_question

app = FastAPI(title="chatbot")

MEMORY_TTL_SECONDS = 30 * 60
MAX_HISTORY_MESSAGES = 10

conversation_memory = {}
memory_lock = Lock()


def get_history(conversation_id: str) -> list[dict]:
    now = time.time()

    with memory_lock:
        conversation = conversation_memory.get(conversation_id)

        if not conversation or now - conversation["last_activity"] > MEMORY_TTL_SECONDS:
            conversation_memory[conversation_id] = {
                "messages": [],
                "last_activity": now
            }
            return []

        conversation["last_activity"] = now
        return conversation["messages"].copy()


def add_to_history(conversation_id: str, role: str, content: str) -> None:
    now = time.time()

    with memory_lock:
        if conversation_id not in conversation_memory:
            conversation_memory[conversation_id] = {
                "messages": [],
                "last_activity": now
            }

        conversation_memory[conversation_id]["messages"].append({
            "role": role,
            "content": content
        })

        conversation_memory[conversation_id]["messages"] = (
            conversation_memory[conversation_id]["messages"][-MAX_HISTORY_MESSAGES:]
        )

        conversation_memory[conversation_id]["last_activity"] = now

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@app.get("/")
def home():
    return {"status": "online"}


@app.post("/chat")
def chat(request: ChatRequest):
    history = get_history(request.conversation_id)
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
    reply = generate_reply(history, request.message)
    
    add_to_history(request.conversation_id, "user", request.message)
    add_to_history(request.conversation_id, "assistant", reply)
    
    return {
        "response": reply
    }