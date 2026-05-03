from openai import OpenAI
from config import OPENAI_API_KEY
from core.utils import logger

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def generate_ai_insight(title: str):
    if not client:
        return {"summary": "", "sentiment": "", "reason": ""}

    try:
        prompt = f"""
Analyze this crypto news headline:

"{title}"

Return:
- Short summary (max 15 words)
- Sentiment (positive/negative/neutral)
- Reason (why it matters)

JSON format only.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        text = response.choices[0].message.content

        import json
        data = json.loads(text)

        return {
            "summary": data.get("summary", ""),
            "sentiment": data.get("sentiment", ""),
            "reason": data.get("reason", "")
        }

    except Exception as e:
        logger.warning(f"⚠️ AI error: {e}")
        return {"summary": "", "sentiment": "", "reason": ""}
