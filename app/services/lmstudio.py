from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

SYSTEM_PROMPT = """
You are a STRICT binary classifier.

Detect the user's language automatically.

Your task is ONLY to classify the message, NEVER answer it.

Reply with EXACTLY one token:
AUTO
NON_AUTO

AUTO:
- cars, automobiles, vehicles
- engines, transmissions
- diagnostics, OBD, error codes
- maintenance, oil, brakes, tires, batteries
- fuel, suspension, cooling, service, spare parts

NON_AUTO:
- programming, IT, school, history, medicine, finance
- general conversation
- any topic unrelated to automobiles
- any question about life who i am or who u are 

Rules:
- Never explain.
- Never translate.
- Never answer the user's question.
- Output ONLY AUTO or NON_AUTO.
"""

def classify_question(question: str) -> str:
    response = client.chat.completions.create(
        model="qwen2.5-1.5b-instruct",
        temperature=0,
        max_tokens=2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    # Dacă LM Studio nu întoarce text
    if not response.choices or response.choices[0].message.content is None:
        return "NON_AUTO"

    answer = response.choices[0].message.content.strip().upper()

    print(f"LM RAW: [{answer}]")

    answer = (response.choices[0].message.content or "").strip().upper()
    
    print("RAW:", answer)
    
    if answer == "AUTO":
        return "AUTO"
    
    # orice alt răspuns este considerat NON_AUTO
    return "NON_AUTO"