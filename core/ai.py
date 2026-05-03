from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def generate_ai_insight(title):
    if not client:
        return ""

    try:
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": f"Summarize this crypto news in 10 words: {title}"
            }]
        )

        return res.choices[0].message.content.strip()

    except Exception:
        return ""
