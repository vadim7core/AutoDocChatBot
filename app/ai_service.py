import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")



def generate_reply(history: list[dict], message: str) -> str:
    
    print(">>> DEEPSEEK A FOST APELAT <<<")
     
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful and knowledgeable AI assistant. "
                    "Answer any question accurately, clearly, and concisely. "
                    "Always reply in the same language as the user's message. "
                )
            },
            *history,
            {
                "role": "user",
                "content": message
            }
        ]

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.5
    }
    
    try:
        response = httpx.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Eroare AI: {str(e)}"