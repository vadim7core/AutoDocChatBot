from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

SYSTEM_PROMPT = """
Ești un clasificator binar STRICT.

Răspunde EXCLUSIV cu unul dintre aceste două cuvinte:
AUTO
NON_AUTO

AUTO = întrebări despre automobile, motoare, piese, service, diagnoză, anvelope, combustibil și întreținere.

NON_AUTO = orice alt subiect.

Exemple:
Cum schimb uleiul la BMW? -> AUTO
Ce este Java? -> NON_AUTO
Ce face mama? -> NON_AUTO

Nu explica nimic.
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

    answer = response.choices[0].message.content.strip().upper()

    print(f"LM RAW: [{answer}]")

    if answer.startswith("NON_AUTO"):
        return "NON_AUTO"

    return "AUTO"