import difflib
from config import SIMILARITY_THRESHOLD, IMPORTANT_KEYWORDS
from core.utils import safe_html
from core.ai import generate_ai_insight

# ============================
# Filtering
# ============================

def is_important(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in IMPORTANT_KEYWORDS)

# ============================
# Duplicate detection
# ============================

def is_duplicate(title: str, recent_titles: list):
    title = title.lower()

    for prev in recent_titles[-100:]:
        prev = prev.lower()

        if title == prev:
            return True

        if title in prev or prev in title:
            return True

        if difflib.SequenceMatcher(None, title, prev).ratio() >= SIMILARITY_THRESHOLD:
            return True

    return False

# ============================
# Sentiment (fast)
# ============================

def analyze_sentiment(title: str):
    t = title.lower()

    if any(x in t for x in ["surge", "pump", "bull", "rally", "gain"]):
        return "🟢"
    if any(x in t for x in ["crash", "dump", "hack", "drop", "fall"]):
        return "🔴"
    return "🟡"

# ============================
# Format message + AI
# ============================

def format_message(item: dict):
    title  = item["title"]
    url    = item["url"]
    source = item["source"]

    sentiment = analyze_sentiment(title)

    # AI insight
    ai = generate_ai_insight(title)

    msg = f"{sentiment} <b>{safe_html(title)}</b>\n\n"

    if ai["summary"]:
        msg += f"🧠 <b>Insight:</b> {safe_html(ai['summary'])}\n"

    msg += f"\n📰 {source}\n🔗 {url}"

    return msg
