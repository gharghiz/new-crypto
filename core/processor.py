import difflib
from config import IMPORTANT_KEYWORDS, SIMILARITY_THRESHOLD
from core.utils import safe_html
from core.ai import generate_ai_insight
from services.market import get_market_data


def is_important(title):
    t = title.lower()
    return any(k in t for k in IMPORTANT_KEYWORDS)


def is_duplicate(title, recent_titles):
    for prev in recent_titles[-50:]:
        if difflib.SequenceMatcher(None, title, prev).ratio() >= SIMILARITY_THRESHOLD:
            return True
    return False


def format_message(item):
    title = item["title"]

    msg = f"📰 <b>{safe_html(title)}</b>\n\n"

    ai = generate_ai_insight(title)
    if ai:
        msg += f"🧠 {ai}\n\n"

    market = get_market_data(title)
    if market:
        msg += f"💰 {market['price']}\n"
        msg += f"📊 {market['change_1h']} | {market['change_24h']}\n\n"

    msg += f"🔗 {item['url']}"

    return msg
