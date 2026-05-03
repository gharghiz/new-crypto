from openai import OpenAI
from config import OPENAI_API_KEY

client = None

if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None


def generate_ai_insight(title):
    if not client:
        return ""

    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": f"Summarize: {title}"
            }]
        )
        return res.choices[0].message.content.strip()

    except Exception:
        return ""
